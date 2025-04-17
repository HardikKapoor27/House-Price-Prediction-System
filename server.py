from flask import Flask, request, jsonify
import util

app = Flask(__name__)

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

if __name__ == "__main__":
    print("Starting Python Flask Server For House Price Prediction....")
    util.load_saved_artifacts()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
