from flask import Blueprint, jsonify, request
from app.models.data_loader import get_patient_data, get_risk_factors, get_lab_results
from app.services.analytics import predict_risk

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/patients', methods=['GET'])
def get_patients():
    """API endpoint to get patient list with optional filtering"""
    risk_level = request.args.get('risk_level')
    return jsonify(get_patient_data(risk_level=risk_level))

@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """API endpoint to get specific patient details"""
    data = get_patient_data(patient_id=patient_id)
    if not data:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(data[0] if isinstance(data, list) else data)

@api_bp.route('/risk-factors', methods=['GET'])
def risk_factors():
    """API endpoint to get risk factors data"""
    return jsonify(get_risk_factors())

@api_bp.route('/lab-results/<int:patient_id>', methods=['GET'])
def lab_results(patient_id):
    """API endpoint to get lab results for a patient"""
    results = get_lab_results(patient_id)
    if not results:
        return jsonify({'error': 'No lab results found'}), 404
    return jsonify(results)

@api_bp.route('/predict', methods=['POST'])
def predict():
    """API endpoint to predict heart attack risk based on input data"""
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400
    
    patient_data = request.json
    risk_prediction = predict_risk(patient_data)
    
    return jsonify({
        'prediction': risk_prediction,
        'timestamp': 'current_date_placeholder'  # Replace with actual datetime
    })
