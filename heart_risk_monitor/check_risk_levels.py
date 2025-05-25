import sqlite3

def check_risk_levels():
    """Check what risk levels exist in the RiskAssessment table"""
    try:
        # Connect to the database
        conn = sqlite3.connect('C:/Users/samuel/Desktop/new-project-main/capstone2_project.db')
        cursor = conn.cursor()
        
        # Check unique risk levels
        cursor.execute("SELECT DISTINCT HeartAttackRiskText FROM RiskAssessment")
        risk_levels = cursor.fetchall()
        print(f"Available risk levels: {[level[0] for level in risk_levels]}")
        
        # Count patients by risk level
        for level in [level[0] for level in risk_levels]:
            cursor.execute(f"SELECT COUNT(*) FROM RiskAssessment WHERE HeartAttackRiskText=?", (level,))
            count = cursor.fetchone()[0]
            print(f"Patients with risk level '{level}': {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking risk levels: {str(e)}")

if __name__ == "__main__":
    check_risk_levels()
