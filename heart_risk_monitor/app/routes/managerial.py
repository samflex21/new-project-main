from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np
import sqlite3

# Import the function to get accurate patient counts
from app.services.patient_counts import get_accurate_patient_counts

# Import the new population health data functions
from app.models.population_health import (
    get_health_risk_by_income,
    get_diet_score_by_age,
    get_exercise_sleep_distribution,
    get_smoking_stress_by_gender
)

# Import data loader functions if available, otherwise use mock data
try:
    from app.models.data_loader import get_population_data, get_resource_utilization
    from app.services.analytics import calculate_population_metrics
    USE_MOCK_DATA = False
except ImportError:
    USE_MOCK_DATA = True
    
    # Mock data functions
    def get_population_data(demographic=None, time_period=None):
        # Return mock population data
        return [
            {
                'demographic': 'Age 50-65',
                'count': 120,
                'high_risk_percentage': 23.5,
                'medium_risk_percentage': 35.0,
                'low_risk_percentage': 41.5
            },
            {
                'demographic': 'Age 65+',
                'count': 85,
                'high_risk_percentage': 32.9,
                'medium_risk_percentage': 40.0,
                'low_risk_percentage': 27.1
            },
            {
                'demographic': 'Male',
                'count': 105,
                'high_risk_percentage': 28.6,
                'medium_risk_percentage': 38.1,
                'low_risk_percentage': 33.3
            },
            {
                'demographic': 'Female',
                'count': 100,
                'high_risk_percentage': 25.0,
                'medium_risk_percentage': 37.0,
                'low_risk_percentage': 38.0
            }
        ]
    
    def get_resource_utilization():
        # Return mock resource utilization data
        return [
            {'resource': 'Cardiology', 'utilization': 78.5},
            {'resource': 'Emergency', 'utilization': 65.2},
            {'resource': 'Imaging', 'utilization': 82.1},
            {'resource': 'Lab Tests', 'utilization': 91.0}
        ]
    
    def calculate_population_metrics(population_data):
        # Return mock population metrics
        return {
            'total_patients': 205,
            'high_risk_count': 54,
            'medium_risk_count': 78,
            'low_risk_count': 73,
            'demographic_breakdown': {
                'male': 105,
                'female': 100,
                'age_groups': {
                    '50-65': 120,
                    '65+': 85
                }
            },
            'trends': {
                'last_month': {
                    'high_risk': 26.3,
                    'medium_risk': 38.0,
                    'low_risk': 35.7
                },
                'current_month': {
                    'high_risk': 26.8,
                    'medium_risk': 37.1,
                    'low_risk': 36.1
                }
            }
        }

managerial_bp = Blueprint('managerial', __name__, url_prefix='/managerial')

@managerial_bp.route('/')
def dashboard():
    """Render the managerial dashboard for population health officials"""
    # Get accurate patient counts directly from the database
    patient_counts = get_accurate_patient_counts()
    
    # Get sample data for other visualizations
    population_data = get_population_data()
    resource_data = get_resource_utilization()
    population_metrics = calculate_population_metrics(population_data)
    
    # Update metrics with accurate patient counts
    population_metrics['total_patients'] = patient_counts['total_patients']
    population_metrics['high_risk_count'] = patient_counts['high_risk_count']
    population_metrics['medium_risk_count'] = patient_counts['medium_risk_count']
    population_metrics['low_risk_count'] = patient_counts['low_risk_count']
    
    # Get data for the health indicator charts
    health_risk_income_data = get_health_risk_by_income()
    diet_score_age_data = get_diet_score_by_age()
    exercise_sleep_data = get_exercise_sleep_distribution()
    smoking_stress_data = get_smoking_stress_by_gender()
    
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
                               'patient_counts': patient_counts  # Add the accurate counts
                           })

@managerial_bp.route('/data')
def dashboard_data():
    """API endpoint to fetch data for the managerial dashboard"""
    # Get filters from request
    department = request.args.get('department')
    time_period = request.args.get('time_period')
    population_segment = request.args.get('population_segment')
    
    # Get filtered data
    population_data = get_population_data(department, time_period, population_segment)
    
    # Calculate metrics for visualizations
    metrics = calculate_population_metrics(population_data)
    
    return jsonify({
        'population_data': population_data,
        'metrics': metrics
    })
