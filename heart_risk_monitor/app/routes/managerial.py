from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np

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
    """Render the managerial dashboard for hospital administrators"""
    # Get sample data for initial render
    population_data = get_population_data()
    resource_data = get_resource_utilization()
    population_metrics = calculate_population_metrics(population_data)
    
    return render_template('managerial.html', 
                           title='Population Health Insights',
                           sample_data={
                               'population': population_data,
                               'resources': resource_data,
                               'metrics': population_metrics
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
