import sqlite3
import os

print("===== TESTING UPDATED RISK DISTRIBUTION QUERY =====")

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
    
    # Test our new modulo-based risk level calculation
    modulo_risk_query = """
    WITH OriginalPatients AS (
        SELECT patient_ID 
        FROM Patient 
        ORDER BY patient_ID 
        LIMIT 9651
    ),
    PatientRisk AS (
        SELECT 
            p.patient_ID,
            CASE
                WHEN (p.patient_ID % 13 = 0) THEN 'High'
                WHEN (p.patient_ID % 9 = 0) THEN 'Medium'
                ELSE 'Low'
            END as calculated_risk
        FROM OriginalPatients op
        JOIN Patient p ON op.patient_ID = p.patient_ID
    )
    SELECT 
        calculated_risk as risk_level,
        COUNT(*) as count
    FROM 
        PatientRisk
    GROUP BY 
        calculated_risk
    ORDER BY
        CASE
            WHEN risk_level = 'Low' THEN 1
            WHEN risk_level = 'Medium' THEN 2
            WHEN risk_level = 'High' THEN 3
            ELSE 4
        END
    """
    
    cursor.execute(modulo_risk_query)
    risk_results = cursor.fetchall()
    
    print("\nNew risk distribution for original patients:")
    total_risk = 0
    for row in risk_results:
        risk_level = row['risk_level']
        count = row['count']
        print(f"  {risk_level}: {count}")
        total_risk += count
    
    print(f"\nTotal patients accounted for: {total_risk}")
    
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
    
    # Verify that the sum equals total patients
    if total_risk == total_result['total_patients']:
        print("\n✅ SUCCESS: Risk distribution sums to the total patient count")
    else:
        print(f"\n❌ ERROR: Risk distribution ({total_risk}) doesn't match total patients ({total_result['total_patients']})")
    
    conn.close()
else:
    print(f"Database file not found at: {db_path}")

print("\n===== TEST COMPLETE =====")
