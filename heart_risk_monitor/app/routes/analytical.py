from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np

# Import data loader functions if available, otherwise use mock data
try:
    from app.models.data_loader import get_patient_data, get_risk_distribution
    from app.services.analytics import calculate_risk_metrics
    USE_MOCK_DATA = False
except ImportError:
    USE_MOCK_DATA = True
    
    # Mock data functions
    def get_patient_data(patient_id=None, risk_level=None, date_range=None):
        # Return mock patient data
        return [
            {
                'patient_ID': 101,
                'age': 65,
                'gender': 'Male',
                'SystolicBP': 165,
                'DiastolicBP': 95,
                'HeartRate': 88,
                'BMI': 32.1,
                'Cholesterol': 245,
                'BloodSugar': 130,
                'risk_level': 'High'
            },
            {
                'patient_ID': 102,
                'age': 58,
                'gender': 'Female',
                'SystolicBP': 155,
                'DiastolicBP': 92,
                'HeartRate': 85,
                'BMI': 30.2,
                'Cholesterol': 235,
                'BloodSugar': 125,
                'risk_level': 'High'
            }
        ]
    
    def get_risk_distribution():
        # Return mock risk distribution
        return [
            {'risk_level': 'Low', 'count': 54},
            {'risk_level': 'Medium', 'count': 42},
            {'risk_level': 'High', 'count': 28}
        ]
    
    def calculate_risk_metrics(patient_data):
        # Return mock risk metrics
        return {
            'avg_risk_score': 65.3,
            'risk_distribution': {
                'high': 28,
                'medium': 42,
                'low': 54
            },
            'vital_stats': {
                'avg_bmi': 28.4,
                'avg_systolic': 138.2,
                'avg_diastolic': 90.1,
                'avg_heart_rate': 85.3
            },
            'lab_stats': {
                'avg_cholesterol': 220.6,
                'avg_blood_sugar': 110.2
            }
        }

analytical_bp = Blueprint('analytical', __name__, url_prefix='/analytical')

@analytical_bp.route('/')
def dashboard():
    """Render the analytical dashboard for healthcare providers"""
    # Get sample data for initial render
    sample_patients = get_patient_data()
    sample_risk = get_risk_distribution()
    sample_metrics = calculate_risk_metrics(sample_patients)
    
    return render_template('analytical.html', 
                           title='Patient Risk Monitoring',
                           sample_data={
                               'patients': sample_patients,
                               'risk_distribution': sample_risk,
                               'metrics': sample_metrics
                           })

@analytical_bp.route('/data')
def dashboard_data():
    """API endpoint to fetch data for the analytical dashboard"""
    # Get filters from request
    patient_id = request.args.get('patient_id')
    risk_level = request.args.get('risk_level')
    date_range = request.args.get('date_range')
    
    # Get filtered data
    patient_data = get_patient_data(patient_id, risk_level, date_range)
    risk_distribution = get_risk_distribution()
    
    # Calculate metrics for visualizations
    metrics = calculate_risk_metrics(patient_data)
    
    return jsonify({
        'patient_data': patient_data,
        'risk_distribution': risk_distribution,
        'metrics': metrics
    })
