from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import json
from util import get_estimated_price, get_location_names, load_saved_artifacts
from database import create_tables
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CORS(app, supports_credentials=True, origins=["https://hardikkapoor27.github.io"],resources={r"/prediction-history": {"origins": "https://hardikkapoor27.github.io"}})
load_saved_artifacts()  # Load model & data columns
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True
)

class CustomSessionInterface(SecureCookieSessionInterface):
    def save_session(self, *args, **kwargs):
        super().save_session(*args, **kwargs)

app.session_interface = CustomSessionInterface()

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = 'https://hardikkapoor27.github.io'
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Allow-Headers'] = 'Content-Type'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        
        return response

# ----------- Helper Functions -----------
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------- User Auth Routes -----------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = hash_password(data['password'])

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return jsonify({'status': 'success'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Email already exists'})
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = hash_password(data['password'])

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['name'] = user['name']
        return jsonify({'status': 'success', 'name': user['name'], 'email': user['email']})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/account', methods=['GET'])
def account():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    return jsonify({
        'status': 'success',
        'user': {
            'name': session['name'],
            'email': session['email']
        }
    })
    
# ----------- Prediction & History Routes -----------
@app.route('/save-prediction', methods=['POST'])
def save_prediction():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    data = request.get_json()
    input_data = data['input_data']
    predicted_price = data['predicted_price']
    user_id = session['user_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predictions (user_id, input_data, predicted_price) VALUES (?, ?, ?)", 
                   (user_id, input_data, predicted_price))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

import json

@app.route('/prediction-history', methods=['GET'])
def prediction_history():
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT input_data, predicted_price, timestamp FROM predictions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    predictions = []
    for row in rows:
        input_data = json.loads(row[0])  # row[0] is input_data JSON string
        predictions.append({
            'location': input_data.get('location'),
            'total_sqft': input_data.get('total_sqft'),
            'bhk': input_data.get('bhk'),
            'bath': input_data.get('bath'),
            'predicted_price': row[1],
            'timestamp': row[2]
        })

    conn.close()

    return jsonify({'status': 'success', 'predictions': predictions})

# ----------- ML Prediction API -----------
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input format'}), 400

    try:
        total_sqft = float(data['total_sqft'])
        bhk = int(data['bhk'])
        bath = int(data['bath'])
        location = data['location']
        estimated_price = get_estimated_price(location, total_sqft, bhk, bath)  # <- MISSING!
        return jsonify({'estimated_price': estimated_price})
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid input values'}), 400


@app.route('/get_location_names', methods=['GET'])
def get_location_names_api():
    locations = get_location_names()
    return jsonify({'locations': locations})

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://hardikkapoor27.github.io'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# ----------- Run the App -----------
if __name__ == '__main__':
    create_tables()
    print("Starting Python Flask Server For House Price Prediction....")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
