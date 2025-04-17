from flask import Flask, request, jsonify
from flask_cors import CORS

import util

app = Flask(__name__)
users_db = {}
prediction_history = []

CORS(app, resources={r"/*": {"origins": "https://hardikkapoor27.github.io"}})

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    return response

@app.route('/predict_house_price', methods=['POST'])
def predict_house_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    email = request.form['email']  # Get from frontend form

    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    prediction = {
        'location': location,
        'total_sqft': total_sqft,
        'bhk': bhk,
        'bath': bath,
        'estimated_price': estimated_price
    }

    if email in users_db:
        if 'history' not in users_db[email]:
            users_db[email]['history'] = []
        users_db[email]['history'].append(prediction)

    return jsonify({'estimated_price': estimated_price})
    return response

@app.route('/get_account_info', methods=['POST'])
def get_account_info():
    data = request.json
    email = data.get("email")

    user = users_db.get(email)
    if user:
        return jsonify({
            "success": True,
            "email": user["email"],
            "password": user["password"],
            "history": user.get("history", [])
        })
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

@app.route('/get_prediction_history', methods=['POST'])
def get_prediction_history():
    data = request.json
    email = data.get("email")

    user = users_db.get(email)
    if user:
        history = user.get("history", [])
        return jsonify({"success": True, "prediction_history": history})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    if email in users_db:
        return jsonify({"success": False, "message": "User already exists"}), 409

    users_db[email] = {"email": email, "password": password}
    return jsonify({"success": True, "message": "Registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    user = users_db.get(email)
    if user and user["password"] == password:
        return jsonify({"success": True, "message": "Login successful", "email": user["email"]}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.before_request
def before_request():
    if request.method == "OPTIONS":
        response = app.make_response('')
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

if __name__ == "__main__":
    print("Starting Python Flask Server For House Price Prediction....")
    util.load_saved_artifacts()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
