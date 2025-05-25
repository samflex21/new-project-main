import sqlite3
import os

print("===== TESTING UPDATED QUERIES =====")

# Database connection
db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
if os.path.exists(db_path):
    print(f"Database found at: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Test total patients query (limited to original 9651)
    total_query = """
    SELECT COUNT(DISTINCT patient_ID) as total_patients FROM Patient
    WHERE patient_ID IN (SELECT patient_ID FROM Patient ORDER BY patient_ID LIMIT 9651)
    """
    cursor.execute(total_query)
    total_result = cursor.fetchone()
    print(f"\nTotal patients query returned: {total_result['total_patients']}")
    
    # Test risk levels query with limit
    risk_query = """
    SELECT 
        CASE
            WHEN HeartAttackRiskText IN ('high', 'High', 'HIGH', 'High Risk', 'high risk') THEN 'High'
            WHEN HeartAttackRiskText IN ('medium', 'Medium', 'MEDIUM', 'Medium Risk', 'medium risk') THEN 'Medium'
            WHEN HeartAttackRiskText IN ('low', 'Low', 'LOW', 'Low Risk', 'low risk') THEN 'Low'
            ELSE 'Unknown'
        END as risk_level,
        COUNT(*) as count
    FROM 
        RiskAssessment
    WHERE
        HeartAttackRiskText IS NOT NULL AND 
        HeartAttackRiskText != '' AND
        PatientID IN (SELECT patient_ID FROM Patient ORDER BY patient_ID LIMIT 9651)
    GROUP BY 
        risk_level
    ORDER BY
        CASE
            WHEN risk_level = 'Low' THEN 1
            WHEN risk_level = 'Medium' THEN 2
            WHEN risk_level = 'High' THEN 3
            ELSE 4
        END
    """
    cursor.execute(risk_query)
    risk_results = cursor.fetchall()
    
    print("\nRisk levels for original patients only:")
    total_risk = 0
    for row in risk_results:
        risk_level = row['risk_level']
        count = row['count']
        print(f"  {risk_level}: {count}")
        total_risk += count
    
    print(f"\nTotal risk assessments for original patients: {total_risk}")
    
    # Calculate expected values for dashboard
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for row in risk_results:
        if row['risk_level'] == 'High':
            high_count = row['count']
        elif row['risk_level'] == 'Medium':
            medium_count = row['count']
        elif row['risk_level'] == 'Low':
            low_count = row['count']
    
    print("\nExpected dashboard values:")
    print(f"  Total patients: {total_result['total_patients']}")
    print(f"  High risk patients: {high_count}")
    print(f"  Medium risk patients: {medium_count}")
    print(f"  Low risk patients: {low_count}")
    
    conn.close()
else:
    print(f"Database file not found at: {db_path}")

print("\n===== TEST COMPLETE =====")
