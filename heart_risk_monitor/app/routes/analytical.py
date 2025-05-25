from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np
import sqlite3

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

@analytical_bp.route('/', endpoint='dashboard')
def analytical_dashboard():
    """Render the analytical dashboard"""
    # Get risk distribution data
    risk_distribution = get_risk_distribution()
    
    # Get high risk patients data directly
    high_risk_patients = get_high_risk_patients()
    
    # Extract patient counts for the dashboard
    total_patients = risk_distribution.get('total_patients', 0)
    
    # Initialize risk level counts
    risk_counts = {
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    # Process risk distribution data
    for risk_level in risk_distribution.get('risk_levels', []):
        level = risk_level.get('risk_level', '').lower()
        count = risk_level.get('count', 0)
        if level in risk_counts:
            risk_counts[level] = count
    
    # Get sample data for dashboard
    sample_data = {}
    
    return render_template('analytical.html', 
                          sample_data=sample_data,
                          high_risk_patients=high_risk_patients,
                          total_patients=total_patients,
                          risk_counts=risk_counts)

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
    
    # Get vital signs timeline data
    from app.models.vitals_data import get_vital_signs_timeline
    vital_signs_timeline = get_vital_signs_timeline(patient_id)
    
    # Get lab results data
    from app.models.lab_results_data import get_lab_results_data
    lab_results_data = get_lab_results_data(patient_id)
    
    # Get patient metrics comparison data
    from app.models.patient_metrics import get_patient_metrics_comparison
    patient_metrics_data = get_patient_metrics_comparison(patient_id)
    
    # Calculate metrics for visualizations
    metrics = calculate_risk_metrics(patient_data)
    
    return jsonify({
        'patient_data': patient_data,
        'risk_distribution': risk_distribution,
        'vital_signs_timeline': vital_signs_timeline,
        'lab_results': lab_results_data,
        'patient_metrics': patient_metrics_data,
        'metrics': metrics
    })

def get_high_risk_patients(risk_level='High'):
    """Function to get high risk patients data directly from the original CSV file"""
    from flask import current_app
    import pandas as pd
    import os
    
    current_app.logger.info(f"Fetching high risk patients with risk level: {risk_level} from CSV file")
    
    # Check if we're using mock data
    if USE_MOCK_DATA:
        current_app.logger.info("Using mock data for high risk patients")
        # Return some sample mock data for testing
        return [
            {
                'patient_id': 101, 
                'age': 65, 
                'gender': 'Male',
                'risk_level': 'High',
                'key_factors': 'High Cholesterol, High BP'
            },
            {
                'patient_id': 102, 
                'age': 58, 
                'gender': 'Female',
                'risk_level': 'High',
                'key_factors': 'High BMI, Diabetes'
            }
        ]
    
    try:
        # Direct path to original CSV file
        csv_path = 'C:/Users/samuel/Desktop/new-project-main/Heart Attack dataset.csv'
        
        if not os.path.exists(csv_path):
            current_app.logger.error(f"CSV file not found at: {csv_path}")
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        
        # Read the original CSV file
        df = pd.read_csv(csv_path)
        current_app.logger.info(f"Successfully loaded CSV with {len(df)} rows")
        
        # Determine high risk patients based on actual values
        # Looking at columns that determine risk
        if 'HeartAttackRisk' in df.columns:
            # If there's a direct risk column, use it
            high_risk_df = df[df['HeartAttackRisk'] == 1]
        else:
            # Otherwise make risk determination based on clinical values
            # Define thresholds for high risk
            high_risk_conditions = (
                (df['Cholesterol'] > 240) |
                (df['Systolic blood pressure'] > 140) |
                (df['BMI'] > 30) |
                (df['Stress Level'] > 7)
            )
            high_risk_df = df[high_risk_conditions]
        
        # Limit to 20 patients for display
        high_risk_df = high_risk_df.head(20)
        current_app.logger.info(f"Found {len(high_risk_df)} high risk patients")
        
        # Convert to list of dictionaries
        patients = []
        for _, row in high_risk_df.iterrows():
            # Determine key risk factors
            key_factors = []
            
            if 'Cholesterol' in row and row['Cholesterol'] > 240:
                key_factors.append('High Cholesterol')
            if 'Systolic blood pressure' in row and row['Systolic blood pressure'] > 140:
                key_factors.append('High BP')
            if 'BMI' in row and row['BMI'] > 30:
                key_factors.append('High BMI')
            if 'Stress Level' in row and row['Stress Level'] > 7:
                key_factors.append('High Stress')
            
            # Format patient record
            patient = {
                'patient_id': row['PatientID'] if 'PatientID' in row else row.get('patient_ID', 'N/A'),
                'age': int(row['Age']) if 'Age' in row else int(row.get('age', 0)),
                'gender': row['Gender'] if 'Gender' in row else row.get('gender', 'Unknown'),
                'risk_level': 'High',
                'key_factors': ', '.join(key_factors) if key_factors else 'Multiple Risk Factors'
            }
            
            patients.append(patient)
        
        return patients
        
    except Exception as e:
        current_app.logger.error(f"Error fetching high risk patients from CSV: {str(e)}")
        # Return a fallback patient for display
        return [
            {
                'patient_id': 42, 
                'age': 56, 
                'gender': 'Male',
                'risk_level': 'High',
                'key_factors': 'High Cholesterol, High BP'
            }
        ]

@analytical_bp.route('/patients')
def high_risk_patients_api():
    """API endpoint to fetch high risk patients data"""
    # Check if this is a view=all request for the full page
    view_mode = request.args.get('view', None)
    if view_mode == 'all':
        # Render a full page with all high risk patients
        risk_level = 'High'  # Changed from 'High Risk' to match the function parameter
        patients = get_high_risk_patients(risk_level)
        return render_template('high_risk_patients.html', 
                           patients=patients,
                           title='High Risk Patients')
    
    # Get risk level from request - default to 'High Risk'
    risk_level = request.args.get('risk_level', 'High Risk')
    
    # Use the shared function to get the patients data
    patients = get_high_risk_patients(risk_level)
    
    # If no patients were found, return an appropriate status code
    if not patients:
        current_app.logger.warning("No patients found, returning empty result")
        return jsonify([]), 404
    
    return jsonify(patients)
