from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load fraud data from a CSV file
fraud_data = pd.read_csv('../docs/merged_fraud_data.csv')

@app.route('/summary', methods=['GET'])
def summary():
    total_transactions = int(fraud_data.shape[0])
    fraud_cases = int(fraud_data['class'].sum())  # Assuming 'class' column is 1 for fraud cases
    fraud_percentage = float((fraud_cases / total_transactions) * 100)
    
    summary_stats = {
        'total_transactions': total_transactions,
        'fraud_cases': fraud_cases,
        'fraud_percentage': fraud_percentage
    }
    return jsonify(summary_stats)

@app.route('/fraud_trends', methods=['GET'])
def fraud_trends():
    fraud_trend = fraud_data.groupby('purchase_time').sum()['class'].reset_index()
    fraud_trend['class'] = fraud_trend['class'].astype(int)  # Convert to int
    fraud_trend['purchase_time'] = fraud_trend['purchase_time'].astype(str)  # Ensure datetime or any other type is converted to string
    
    return fraud_trend.to_json(orient='records')

@app.route('/fraud_geography', methods=['GET'])
def fraud_geography():
    fraud_geo = fraud_data.groupby('country').sum()['class'].reset_index()
    fraud_geo['class'] = fraud_geo['class'].astype(int)  # Convert to int
    
    return fraud_geo.to_json(orient='records')

@app.route('/fraud_device_browser', methods=['GET'])
def fraud_device_browser():
    fraud_device = fraud_data.groupby('device_id').sum()['class'].reset_index()
    fraud_device['class'] = fraud_device['class'].astype(int)  # Convert to int
    
    fraud_browser = fraud_data.groupby('browser').sum()['class'].reset_index()
    fraud_browser['class'] = fraud_browser['class'].astype(int)  # Convert to int
    return fraud_device.to_json(orient='records')
    # return jsonify({
    #     'fraud_device': fraud_device.to_json(orient='records'),
    #     'fraud_browser': fraud_browser.to_json(orient='records')
    # })

if __name__ == '__main__':
    app.run(debug=True)
