import sqlite3
import json

def test_high_risk_query():
    """Test the high risk patients query directly"""
    try:
        # Connect to the database
        conn = sqlite3.connect('C:/Users/samuel/Desktop/new-project-main/capstone2_project.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Execute the exact query from our API endpoint
        query = """
        SELECT 
            p.patient_ID as patient_id, 
            p.age as age, 
            p.gender as gender,
            p.income as income,
            ra.HeartAttackRiskText as risk_level,
            ra.HeartAttackRiskBinary as risk_binary,
            ra.StressLevel as stress_level,
            vs.SystolicBP, 
            vs.DiastolicBP, 
            vs.HeartRate, 
            vs.BMI,
            lr.Cholesterol,
            lr.BloodSugar,
            ls.Smoking,
            ls.AlcoholConsumption,
            ls.ExerciseHoursPerWeek,
            ls.SleepHoursPerDay,
            ls.Diet,
            mh.Diabetes,
            mh.FamilyHistory,
            mh.PreviousHeartProblems
        FROM 
            Patient p
        JOIN 
            RiskAssessment ra ON p.patient_ID = ra.PatientID
        JOIN 
            VitalSigns vs ON p.patient_ID = vs.PatientID
        JOIN 
            LabResults lr ON p.patient_ID = lr.PatientID
        LEFT JOIN
            Lifestyle ls ON p.patient_ID = ls.PatientID
        LEFT JOIN
            MedicalHistory mh ON p.patient_ID = mh.PatientID
        WHERE 
            ra.HeartAttackRiskText = ?
        ORDER BY p.patient_ID
        LIMIT 20
        """
        
        # Execute with the exact parameter
        risk_level = "High Risk"
        cursor.execute(query, (risk_level,))
        
        # Convert results to list of dictionaries
        results = [dict(row) for row in cursor.fetchall()]
        print(f"Query returned {len(results)} patients")
        
        if results:
            # Print the first patient data
            print("\nFirst patient data:")
            print(json.dumps(results[0], indent=2))
        else:
            print("No patients found with the query")
            
            # Check if there's any data with a different risk level
            cursor.execute("SELECT DISTINCT HeartAttackRiskText FROM RiskAssessment LIMIT 5")
            levels = cursor.fetchall()
            print(f"\nAvailable risk levels: {[level[0] for level in levels]}")
            
            # Try to fetch data with the most common risk level
            if levels:
                test_level = levels[0][0]
                cursor.execute(query, (test_level,))
                test_results = [dict(row) for row in cursor.fetchall()]
                print(f"Using '{test_level}' found {len(test_results)} patients")
                if test_results:
                    print("\nSample patient data with different risk level:")
                    print(json.dumps(test_results[0], indent=2))
        
        conn.close()
        
    except Exception as e:
        print(f"Error testing query: {str(e)}")

if __name__ == "__main__":
    test_high_risk_query()
