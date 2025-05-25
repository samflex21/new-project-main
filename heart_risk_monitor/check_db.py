import sqlite3

def check_database():
    """Check the database structure and content"""
    try:
        # Connect to the database
        conn = sqlite3.connect('C:/Users/samuel/Desktop/new-project-main/capstone2_project.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        
        # Check Patient table structure
        cursor.execute("PRAGMA table_info(Patient)")
        patient_columns = cursor.fetchall()
        print(f"Patient table columns: {[col[1] for col in patient_columns]}")
        
        # Check RiskAssessment table structure
        cursor.execute("PRAGMA table_info(RiskAssessment)")
        risk_columns = cursor.fetchall()
        print(f"RiskAssessment table columns: {[col[1] for col in risk_columns]}")
        
        # Count patients
        cursor.execute("SELECT COUNT(*) FROM Patient")
        patient_count = cursor.fetchone()[0]
        print(f"Total patients: {patient_count}")
        
        # Count high risk patients
        cursor.execute("SELECT COUNT(*) FROM RiskAssessment WHERE LOWER(HeartAttackRiskText)='high'")
        high_risk_count = cursor.fetchone()[0]
        print(f"High risk patients count: {high_risk_count}")
        
        # Get sample high risk patient data
        cursor.execute("""
        SELECT 
            p.patient_ID, p.age, p.gender,
            ra.HeartAttackRiskText
        FROM 
            Patient p
        JOIN 
            RiskAssessment ra ON p.patient_ID = ra.PatientID
        WHERE 
            LOWER(ra.HeartAttackRiskText) = 'high'
        LIMIT 5
        """)
        sample_patients = cursor.fetchall()
        print(f"Sample high risk patients: {sample_patients}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == "__main__":
    check_database()
