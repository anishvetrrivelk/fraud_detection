from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to access the backend

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload directory exists

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Fraud Detection System Backend!"})

@app.route('/analyze', methods=['POST'])
def analyze_fraud():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Read CSV/XLSX file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        # Rule-based fraud detection: Flag transactions above a threshold
        threshold = 10000  # Example threshold
        df['is_fraud'] = df['amount'] > threshold  # Assuming 'amount' column exists
        fraud_cases = df[df['is_fraud']]

        return jsonify({
            "message": "File processed successfully!",
            "total_transactions": len(df),
            "fraud_cases_detected": len(fraud_cases),
            "fraud_cases": fraud_cases.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
