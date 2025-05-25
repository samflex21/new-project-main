import sqlite3

def get_accurate_patient_counts():
    """
    Query the SQLite database to get accurate patient counts by risk level
    directly from the Heart Attack dataset.csv using the Script-1.sql schema
    
    Returns:
        Dictionary with patient counts by risk level
    """
    # Connect to the SQLite database
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get total patient count
    cursor.execute("SELECT COUNT(*) FROM Patient")
    total_patients = cursor.fetchone()[0]
    
    # Get high risk patient count
    cursor.execute("SELECT COUNT(*) FROM RiskAssessment WHERE LOWER(HeartAttackRiskText) = 'high'")
    high_risk_count = cursor.fetchone()[0]
    
    # Get medium risk patient count
    cursor.execute("SELECT COUNT(*) FROM RiskAssessment WHERE LOWER(HeartAttackRiskText) = 'medium'")
    medium_risk_count = cursor.fetchone()[0]
    
    # Get low risk patient count
    cursor.execute("SELECT COUNT(*) FROM RiskAssessment WHERE LOWER(HeartAttackRiskText) = 'low'")
    low_risk_count = cursor.fetchone()[0]
    
    # Calculate percentage changes (mock data for demonstration)
    # In a real application, these would be calculated from historical data
    high_risk_percent = 35
    medium_risk_percent = 12
    low_risk_percent = 27
    total_percent = 50
    
    conn.close()
    
    return {
        'total_patients': total_patients,
        'total_percent': total_percent,
        'high_risk_count': high_risk_count,
        'high_risk_percent': high_risk_percent,
        'medium_risk_count': medium_risk_count,
        'medium_risk_percent': medium_risk_percent,
        'low_risk_count': low_risk_count,
        'low_risk_percent': low_risk_percent
    }
