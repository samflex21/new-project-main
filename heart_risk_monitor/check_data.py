import sqlite3
import pandas as pd
import os

print("===== DATA SOURCE VERIFICATION =====")

# Check CSV file
csv_path = 'C:/Users/samuel/Desktop/new-project-main/Heart Attack dataset.csv'
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"CSV file found with {len(df)} rows")
    print(f"CSV file has {df['PatientID'].nunique()} unique PatientIDs")
    
    # Check first few patient IDs
    print("\nSample PatientIDs from CSV:")
    print(df['PatientID'].head(5).tolist())
else:
    print(f"CSV file not found at: {csv_path}")

# Check database
db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
if os.path.exists(db_path):
    print(f"\nDatabase found at: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check Patient table
    cursor.execute("SELECT COUNT(*) as count FROM Patient")
    print(f"Database has {cursor.fetchone()['count']} rows in Patient table")
    
    cursor.execute("SELECT COUNT(DISTINCT patient_ID) as count FROM Patient")
    print(f"Database has {cursor.fetchone()['count']} unique patient_IDs in Patient table")
    
    # Check first few patient IDs in database
    cursor.execute("SELECT patient_ID FROM Patient LIMIT 5")
    patient_ids = [row['patient_ID'] for row in cursor.fetchall()]
    print("\nSample patient_IDs from database:")
    print(patient_ids)
    
    # Check risk counts
    print("\nRisk level counts in database:")
    cursor.execute("""
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
        HeartAttackRiskText IS NOT NULL AND HeartAttackRiskText != ''
    GROUP BY 
        risk_level
    ORDER BY
        count DESC
    """)
    
    risk_counts = cursor.fetchall()
    total_risk_count = 0
    for row in risk_counts:
        risk_level = row['risk_level']
        count = row['count']
        print(f"  {risk_level}: {count}")
        total_risk_count += count
    
    print(f"\nTotal risk assessments: {total_risk_count}")
    
    conn.close()
else:
    print(f"Database file not found at: {db_path}")

print("\n===== END VERIFICATION =====")
