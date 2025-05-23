import pandas as pd
import numpy as np
from datetime import datetime

def calculate_risk_metrics(patient_data):
    """
    Calculate risk metrics for the analytical dashboard
    
    Args:
        patient_data: List of patient data dictionaries
    
    Returns:
        Dictionary with calculated metrics
    """
    # Convert to DataFrame for easier processing
    if not patient_data:
        return {
            'avg_risk_score': 0,
            'risk_distribution': {
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'vital_stats': {
                'avg_bmi': 0,
                'avg_systolic': 0,
                'avg_diastolic': 0,
                'avg_heart_rate': 0
            },
            'lab_stats': {
                'avg_cholesterol': 0,
                'avg_blood_sugar': 0
            }
        }
    
    df = pd.DataFrame(patient_data)
    
    # Calculate risk distribution
    risk_counts = {'high': 0, 'medium': 0, 'low': 0}
    if 'risk_level' in df.columns:
        risk_counts = df['risk_level'].str.lower().value_counts().to_dict()
        # Ensure all categories exist
        for level in ['high', 'medium', 'low']:
            if level not in risk_counts:
                risk_counts[level] = 0
    
    # Calculate average vital signs
    vital_stats = {}
    for col, default in [
        ('BMI', 0), 
        ('SystolicBP', 0), 
        ('DiastolicBP', 0), 
        ('HeartRate', 0)
    ]:
        vital_stats[f'avg_{col.lower()}'] = df[col].mean() if col in df.columns else default
    
    # Calculate average lab results
    lab_stats = {}
    for col, default in [
        ('Cholesterol', 0), 
        ('BloodSugar', 0)
    ]:
        lab_stats[f'avg_{col.lower()}'] = df[col].mean() if col in df.columns else default
    
    # Calculate average risk score (simple placeholder calculation)
    # In a real app, this would use a more sophisticated algorithm
    avg_risk_score = 0
    if 'risk_level' in df.columns:
        risk_map = {'high': 3, 'medium': 2, 'low': 1}
        avg_risk_score = df['risk_level'].str.lower().map(risk_map).mean()
    
    return {
        'avg_risk_score': avg_risk_score,
        'risk_distribution': risk_counts,
        'vital_stats': vital_stats,
        'lab_stats': lab_stats
    }

def calculate_population_metrics(population_data):
    """
    Calculate population-level metrics for the managerial dashboard
    
    Args:
        population_data: Dictionary with population data
    
    Returns:
        Dictionary with calculated metrics
    """
    metrics = {
        'age_risk_correlation': [],
        'lifestyle_impact': [],
        'demographic_breakdown': [],
        'trend_analysis': []
    }
    
    # Process age distribution data
    if 'age_distribution' in population_data:
        age_data = population_data['age_distribution']
        if age_data:
            # Convert to DataFrame for easier processing
            age_df = pd.DataFrame(age_data)
            
            # Calculate age-risk correlation
            metrics['age_risk_correlation'] = [
                {
                    'age_group': row['age_group'],
                    'count': row['count'],
                    'avg_bmi': row['avg_bmi'],
                    'avg_systolic': row['avg_systolic']
                } for _, row in age_df.iterrows()
            ]
    
    # Process gender-risk data
    if 'gender_risk' in population_data:
        gender_data = population_data['gender_risk']
        if gender_data:
            # Convert to DataFrame
            gender_df = pd.DataFrame(gender_data)
            
            # Calculate demographic breakdown
            metrics['demographic_breakdown'] = [
                {
                    'gender': row['gender'],
                    'risk_level': row['risk_level'],
                    'count': row['count']
                } for _, row in gender_df.iterrows()
            ]
    
    # Process lifestyle impact data
    if 'lifestyle_impact' in population_data:
        lifestyle_data = population_data['lifestyle_impact']
        if lifestyle_data:
            # Convert to DataFrame
            lifestyle_df = pd.DataFrame(lifestyle_data)
            
            # Calculate lifestyle impact
            metrics['lifestyle_impact'] = [
                {
                    'smoking': row.get('smoking', False),
                    'alcohol': row.get('alcohol', False),
                    'risk_level': row['risk_level'],
                    'count': row['count']
                } for _, row in lifestyle_df.iterrows()
            ]
    
    # Generate mock trend data (in a real app, this would come from historical data)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    metrics['trend_analysis'] = [
        {
            'month': month,
            'high_risk': np.random.randint(10, 30),
            'medium_risk': np.random.randint(30, 60),
            'low_risk': np.random.randint(40, 80)
        } for month in months
    ]
    
    return metrics

def calculate_risk_score(patient_data, include_details=False):
    """
    Calculate risk score for an individual patient
    
    Args:
        patient_data: Dictionary with patient data
        include_details: Whether to include detailed breakdown
    
    Returns:
        Dictionary with risk score and optional details
    """
    # Simple scoring system (placeholder for demonstration)
    # In a real application, this would use a medically validated algorithm
    
    score = 0
    details = {}
    
    # Process as dict or first item if list
    if isinstance(patient_data, list) and patient_data:
        patient = patient_data[0]
    else:
        patient = patient_data
    
    # Check blood pressure
    if 'SystolicBP' in patient:
        systolic = patient['SystolicBP']
        if systolic > 140:
            score += 3
            details['blood_pressure'] = {'value': systolic, 'risk': 'high'}
        elif systolic > 120:
            score += 2
            details['blood_pressure'] = {'value': systolic, 'risk': 'medium'}
        else:
            score += 1
            details['blood_pressure'] = {'value': systolic, 'risk': 'low'}
    
    # Check cholesterol
    if 'Cholesterol' in patient:
        cholesterol = patient['Cholesterol']
        if cholesterol > 240:
            score += 3
            details['cholesterol'] = {'value': cholesterol, 'risk': 'high'}
        elif cholesterol > 200:
            score += 2
            details['cholesterol'] = {'value': cholesterol, 'risk': 'medium'}
        else:
            score += 1
            details['cholesterol'] = {'value': cholesterol, 'risk': 'low'}
    
    # Check blood sugar
    if 'BloodSugar' in patient:
        blood_sugar = patient['BloodSugar']
        if blood_sugar > 126:
            score += 3
            details['blood_sugar'] = {'value': blood_sugar, 'risk': 'high'}
        elif blood_sugar > 100:
            score += 2
            details['blood_sugar'] = {'value': blood_sugar, 'risk': 'medium'}
        else:
            score += 1
            details['blood_sugar'] = {'value': blood_sugar, 'risk': 'low'}
    
    # Check BMI
    if 'BMI' in patient:
        bmi = patient['BMI']
        if bmi > 30:
            score += 3
            details['bmi'] = {'value': bmi, 'risk': 'high'}
        elif bmi > 25:
            score += 2
            details['bmi'] = {'value': bmi, 'risk': 'medium'}
        else:
            score += 1
            details['bmi'] = {'value': bmi, 'risk': 'low'}
    
    # Age factor
    if 'age' in patient:
        age = patient['age']
        if age > 60:
            score += 3
            details['age'] = {'value': age, 'risk': 'high'}
        elif age > 40:
            score += 2
            details['age'] = {'value': age, 'risk': 'medium'}
        else:
            score += 1
            details['age'] = {'value': age, 'risk': 'low'}
    
    # Calculate overall risk level
    max_possible_score = 15  # Based on 5 factors above with max 3 points each
    normalized_score = (score / max_possible_score) * 100
    
    if normalized_score > 70:
        risk_level = 'high'
    elif normalized_score > 40:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    result = {
        'score': normalized_score,
        'risk_level': risk_level,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if include_details:
        result['details'] = details
    
    return result

def predict_risk(patient_data):
    """
    Predict heart attack risk based on input data
    
    Args:
        patient_data: Dictionary with patient features
    
    Returns:
        Dictionary with risk prediction
    """
    # This is a placeholder for a machine learning model
    # In a real application, this would load a trained ML model
    
    # For demonstration, use our risk score calculation
    risk_result = calculate_risk_score(patient_data, include_details=True)
    
    # Add prediction confidence (mock)
    risk_result['confidence'] = 0.85
    risk_result['model_version'] = '1.0.0'
    
    return risk_result
