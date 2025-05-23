import pandas as pd
import numpy as np
from datetime import datetime

def format_risk_level(value, metric_type):
    """
    Format a numeric value into a risk level string
    
    Args:
        value: Numeric value to evaluate
        metric_type: Type of health metric (e.g., 'Cholesterol', 'BMI')
    
    Returns:
        Risk level string ('Low', 'Medium', 'High')
    """
    if metric_type == 'Cholesterol':
        if value < 200:
            return 'Low'
        elif value < 240:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'BloodSugar':
        if value < 100:
            return 'Low'
        elif value < 126:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'SystolicBP':
        if value < 120:
            return 'Low'
        elif value < 140:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'DiastolicBP':
        if value < 80:
            return 'Low'
        elif value < 90:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'BMI':
        if value < 25:
            return 'Low'
        elif value < 30:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'HeartRate':
        if value < 60:
            return 'Low'
        elif value < 100:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'Triglycerides':
        if value < 150:
            return 'Low'
        elif value < 200:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'CK_MB':
        if value < 5:
            return 'Low'
        elif value < 10:
            return 'Medium'
        else:
            return 'High'
    elif metric_type == 'Troponin':
        if value < 0.04:
            return 'Low'
        elif value < 0.1:
            return 'Medium'
        else:
            return 'High'
    else:
        # Default case
        return 'Medium'

def get_color_for_risk(risk_level):
    """
    Get color code for a risk level
    
    Args:
        risk_level: Risk level string ('Low', 'Medium', 'High')
    
    Returns:
        CSS color class
    """
    risk_level = risk_level.lower()
    if risk_level == 'low':
        return 'success'
    elif risk_level == 'medium':
        return 'warning'
    else:
        return 'danger'

def format_timestamp(timestamp):
    """
    Format a timestamp for display
    
    Args:
        timestamp: Timestamp string or datetime object
    
    Returns:
        Formatted date string
    """
    if isinstance(timestamp, str):
        try:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                dt = datetime.strptime(timestamp, '%Y-%m-%d')
            except ValueError:
                return timestamp
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        return str(timestamp)
    
    return dt.strftime('%b %d, %Y at %I:%M %p')

def format_metric_value(value, metric_type):
    """
    Format a metric value with appropriate units
    
    Args:
        value: Numeric value to format
        metric_type: Type of health metric
    
    Returns:
        Formatted string with units
    """
    if pd.isna(value):
        return 'N/A'
        
    if metric_type == 'Cholesterol' or metric_type == 'BloodSugar' or metric_type == 'Triglycerides':
        return f"{value} mg/dL"
    elif metric_type == 'SystolicBP' or metric_type == 'DiastolicBP':
        return f"{value} mmHg"
    elif metric_type == 'BMI':
        return f"{value:.1f} kg/m²"
    elif metric_type == 'HeartRate':
        return f"{value} BPM"
    elif metric_type == 'CK_MB':
        return f"{value} ng/mL"
    elif metric_type == 'Troponin':
        return f"{value} ng/mL"
    else:
        return str(value)

def calculate_percentile(value, dataset, column):
    """
    Calculate percentile of a value within a dataset
    
    Args:
        value: Value to calculate percentile for
        dataset: DataFrame or list of dictionaries containing the data
        column: Column name to use for comparison
    
    Returns:
        Percentile as a value between 0 and 100
    """
    if isinstance(dataset, list):
        # Convert list of dicts to numpy array
        try:
            values = np.array([d[column] for d in dataset if column in d])
        except (KeyError, TypeError):
            return 50  # Default to 50th percentile on error
    elif isinstance(dataset, pd.DataFrame):
        if column in dataset.columns:
            values = dataset[column].values
        else:
            return 50
    else:
        return 50
    
    if len(values) == 0:
        return 50
    
    # Calculate percentile rank
    return np.percentile(np.arange(100), np.searchsorted(np.sort(values), value) / len(values) * 100)

def generate_chart_colors(num_colors):
    """
    Generate a list of visually distinct colors for charts
    
    Args:
        num_colors: Number of colors to generate
    
    Returns:
        List of hex color codes
    """
    base_colors = [
        '#4e73df',  # Primary blue
        '#1cc88a',  # Success green
        '#f6c23e',  # Warning yellow
        '#e74a3b',  # Danger red
        '#36b9cc',  # Info teal
        '#6f42c1',  # Purple
        '#fd7e14',  # Orange
        '#20c9a6',  # Teal
        '#5a5c69',  # Gray
        '#858796'   # Secondary gray
    ]
    
    # If we need more colors than in our base set, generate them
    if num_colors <= len(base_colors):
        return base_colors[:num_colors]
    else:
        # Add additional colors using HSV color space for better distribution
        import colorsys
        
        additional_colors = []
        for i in range(num_colors - len(base_colors)):
            h = i / (num_colors - len(base_colors))
            r, g, b = colorsys.hsv_to_rgb(h, 0.8, 0.9)
            hex_color = '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
            additional_colors.append(hex_color)
            
        return base_colors + additional_colors

def truncate_string(s, max_length=50):
    """
    Truncate a long string with ellipsis
    
    Args:
        s: String to truncate
        max_length: Maximum length before truncation
    
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + '...'
