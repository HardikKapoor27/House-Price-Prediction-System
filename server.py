from flask import Flask, request, jsonify
from flask_cors import CORS

import util

app = Flask(__name__)

users_db = {}
CORS(app, origins=["https://hardikkapoor27.github.io"])

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_house_price', methods = ['POST'])
def predict_house_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    # Get predicted price
    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    # Create prediction record
    prediction = {
        'location': location,
        'total_sqft': total_sqft,
        'bhk': bhk,
        'bath': bath,
        'estimated_price': estimated_price
    }

    # Append to prediction history
    prediction_history.append(prediction)

    # Save updated prediction history
    util.save_prediction_history(prediction_history)

    # Return predicted price as response
    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_prediction_history', methods = ['GET'])
def get_prediction_history():
    response = jsonify({
        'prediction_history': prediction_history
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    if email in users:
        return jsonify({"success": False, "message": "User already exists"}), 409

    users[email] = {"email": email, "password": password}
    return jsonify({"success": True, "message": "Registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    user = users.get(email)
    if user and user["password"] == password:
        return jsonify({"success": True, "message": "Login successful", "email": user["email"]}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.before_request
def before_request():
    if request.method == "OPTIONS":
        response = app.make_response('')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

if __name__ == "__main__":
    print("Starting Python Flask Server For House Price Prediction....")
    util.load_saved_artifacts()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
