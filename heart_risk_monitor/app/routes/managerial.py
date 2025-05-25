from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np

# Import the CSV data provider for real data from the original dataset
from app.services.csv_data_provider import (
    get_population_overview,
    get_health_risk_by_income,
    get_diet_score_by_age,
    get_exercise_sleep_distribution,
    get_smoking_stress_by_gender,
    get_key_risk_factors
)

# Import data loader for population data
from app.models.data_loader import get_population_data

# Create the blueprint
managerial_bp = Blueprint('managerial', __name__, url_prefix='/managerial')

@managerial_bp.route('/')
def dashboard():
    """Render the managerial dashboard for population health officials using real data from CSV"""
    # Get real population overview data from CSV
    population_metrics = get_population_overview()
    
    # Create resource utilization data (since we're focusing on patient data from CSV)
    resource_data = [
        {'resource': 'Cardiology', 'utilization': 78.5},
        {'resource': 'Emergency', 'utilization': 65.2},
        {'resource': 'Imaging', 'utilization': 82.1},
        {'resource': 'Lab Tests', 'utilization': 91.0}
    ]
    
    # Get data for the health indicator charts directly from CSV
    health_risk_income_data = get_health_risk_by_income()
    diet_score_age_data = get_diet_score_by_age()
    exercise_sleep_data = get_exercise_sleep_distribution()
    smoking_stress_data = get_smoking_stress_by_gender()
    key_risk_factors_data = get_key_risk_factors()
    
    # Create a blank population data structure for backward compatibility
    # This would normally come from demographic breakdowns but we're focusing on risk metrics
    population_data = [
        {
            'demographic': 'All Patients',
            'count': population_metrics['total_patients'],
            'high_risk_percentage': population_metrics['high_risk_percentage'],
            'medium_risk_percentage': round((population_metrics['medium_risk_count'] / population_metrics['total_patients']) * 100, 1),
            'low_risk_percentage': round((population_metrics['low_risk_count'] / population_metrics['total_patients']) * 100, 1)
        }
    ]
    
    # Make sure to use the exact property names expected by the frontend charts
    return render_template('managerial.html', 
                           title='Population Health Overview',
                           sample_data={
                               'population': population_data,
                               'resources': resource_data,
                               'metrics': population_metrics,
                               'health_risk_income': health_risk_income_data,
                               'diet_score_age': diet_score_age_data,
                               'exercise_sleep': exercise_sleep_data,
                               'smoking_stress': smoking_stress_data,
                               'key_risk_factors': key_risk_factors_data
                           })

@managerial_bp.route('/data')
def dashboard_data():
    """API endpoint to fetch data for the managerial dashboard"""
    # Get population overview directly from CSV
    population_metrics = get_population_overview()
    
    # Get health indicator chart data
    health_risk_income_data = get_health_risk_by_income()
    diet_score_age_data = get_diet_score_by_age()
    exercise_sleep_data = get_exercise_sleep_distribution()
    smoking_stress_data = get_smoking_stress_by_gender()
    key_risk_factors_data = get_key_risk_factors()
    
    # Maintain backward compatibility with older API structure
    population_data = [
        {
            'demographic': 'All Patients',
            'count': population_metrics['total_patients'],
            'high_risk_percentage': population_metrics['high_risk_percentage'],
            'medium_risk_percentage': round((population_metrics['medium_risk_count'] / population_metrics['total_patients']) * 100, 1),
            'low_risk_percentage': round((population_metrics['low_risk_count'] / population_metrics['total_patients']) * 100, 1)
        }
    ]
    
    return jsonify({
        'population_data': population_data,
        'metrics': population_metrics,
        'health_risk_income': health_risk_income_data,
        'diet_score_age': diet_score_age_data,
        'exercise_sleep': exercise_sleep_data,
        'smoking_stress': smoking_stress_data,
        'key_risk_factors': key_risk_factors_data
    })
