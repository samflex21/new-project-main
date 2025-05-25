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
    
    # Get sample data for dashboard
    sample_data = {}
    
    return render_template('analytical.html', 
                          sample_data=sample_data,
                          high_risk_patients=high_risk_patients)

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

def get_high_risk_patients(risk_level='High Risk'):
    """Function to get high risk patients data"""
    # Add logging to debug the issue
    from flask import current_app
    current_app.logger.info(f"Fetching high risk patients with risk level: {risk_level}")
    
    try:
        # Query database for patients with the specified risk level
        conn = sqlite3.connect('C:/Users/samuel/Desktop/new-project-main/capstone2_project.db')
        conn.row_factory = sqlite3.Row
        
        # Create query to join Patient and RiskAssessment tables
        query = """
        SELECT 
            p.patient_ID as patient_id, 
            p.age as age, 
            p.gender as gender,
            p.income as income,
            ra.HeartAttackRiskText as risk_level,
            ra.HeartAttackRiskBinary as risk_binary,
            ra.StressLevel as stress_level,
            vs.SystolicBP, 
            vs.DiastolicBP, 
            vs.HeartRate, 
            vs.BMI,
            lr.Cholesterol,
            lr.BloodSugar,
            ls.Smoking,
            ls.AlcoholConsumption,
            ls.ExerciseHoursPerWeek,
            ls.SleepHoursPerDay,
            ls.Diet,
            mh.Diabetes,
            mh.FamilyHistory,
            mh.PreviousHeartProblems
        FROM 
            Patient p
        JOIN 
            RiskAssessment ra ON p.patient_ID = ra.PatientID
        JOIN 
            VitalSigns vs ON p.patient_ID = vs.PatientID
        JOIN 
            LabResults lr ON p.patient_ID = lr.PatientID
        LEFT JOIN
            Lifestyle ls ON p.patient_ID = ls.PatientID
        LEFT JOIN
            MedicalHistory mh ON p.patient_ID = mh.PatientID
        WHERE 
            ra.HeartAttackRiskText = ?
        ORDER BY p.patient_ID
        LIMIT 20
        """
        
        cursor = conn.cursor()
        current_app.logger.info(f"Executing query with parameter: {risk_level}")
        cursor.execute(query, (risk_level,))
        
        # Convert results to list of dictionaries
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        current_app.logger.info(f"Found {len(patients)} high risk patients")
        return patients
        
    except Exception as e:
        current_app.logger.error(f"Error fetching high risk patients: {str(e)}")
        return []

@analytical_bp.route('/patients')
def high_risk_patients_api():
    """API endpoint to fetch high risk patients data"""
    # Check if this is a view=all request for the full page
    view_mode = request.args.get('view', None)
    if view_mode == 'all':
        # Render a full page with all high risk patients
        risk_level = 'High Risk'
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
