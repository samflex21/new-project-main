from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.data_loader import get_patient_data, get_patient_history
from app.services.analytics import calculate_risk_score

patient_bp = Blueprint('patient', __name__, url_prefix='/patients')

@patient_bp.route('/')
def patient_list():
    """Render the patient records page"""
    # Get search/filter parameters if any
    search_term = request.args.get('search', '')
    risk_level = request.args.get('risk_level', '')
    
    # Get filtered patient data
    patients = get_patient_data(search=search_term, risk_level=risk_level)
    
    return render_template('patient_records.html', 
                          title='Patient Records',
                          patients=patients,
                          search_term=search_term,
                          risk_level=risk_level)

@patient_bp.route('/<int:patient_id>')
def patient_detail(patient_id):
    """Render the individual patient detail page"""
    # Get patient data
    patient = get_patient_data(patient_id=patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('patient.patient_list'))
    
    # Get patient history
    history = get_patient_history(patient_id)
    
    # Calculate current risk score
    risk_score = calculate_risk_score(patient)
    
    return render_template('patient_detail.html',
                          title=f'Patient {patient_id}',
                          patient=patient,
                          history=history,
                          risk_score=risk_score)

@patient_bp.route('/report/<int:patient_id>')
def generate_report(patient_id):
    """Generate a printable report for a patient"""
    # Get patient data
    patient = get_patient_data(patient_id=patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('patient.patient_list'))
    
    # Get patient history
    history = get_patient_history(patient_id)
    
    # Calculate risk metrics
    risk_metrics = calculate_risk_score(patient, include_details=True)
    
    return render_template('report.html',
                          title=f'Report for Patient {patient_id}',
                          patient=patient,
                          history=history,
                          risk_metrics=risk_metrics)
