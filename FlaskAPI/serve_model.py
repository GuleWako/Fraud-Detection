from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
rf_clf = joblib.load('models/fraud_data_model.pkl')
model = rf_clf 

@app.route('/')
def home():
    return "Welcome to the Fraud Detection API. Use the /predict endpoint to get predictions."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = list(data.values())
    features_array = np.array([features])
    prediction = model.predict(features_array)
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
