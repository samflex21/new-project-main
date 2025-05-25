import sqlite3
import csv
import os
import pandas as pd

def create_db_schema(db_path):
    """Create database schema from SQL script"""
    # Read SQL script
    with open('Script-1.sql', 'r') as sql_file:
        # Read only the schema part (CREATE TABLE statements)
        sql_script = ""
        for line in sql_file:
            if line.strip().startswith('--'):
                continue
            if line.strip().startswith('INSERT'):
                break
            sql_script += line
    
    # Connect to database and execute schema creation
    conn = sqlite3.connect(db_path)
    conn.executescript(sql_script)
    conn.commit()
    print(f"Database schema created at {db_path}")
    return conn

def import_csv_to_sqlite(csv_path, db_path):
    """Import CSV data into SQLite database"""
    # Check if database exists, if not create schema
    if not os.path.exists(db_path):
        conn = create_db_schema(db_path)
    else:
        conn = sqlite3.connect(db_path)
    
    # Read CSV file using pandas for better handling
    df = pd.read_csv(csv_path)
    print(f"CSV loaded successfully with {len(df)} rows")
    
    # Create cursor
    cursor = conn.cursor()
    
    # Clear existing data (if any)
    tables = ['Patient', 'VitalSigns', 'LabResults', 'Lifestyle', 
             'MedicalHistory', 'RiskAssessment', 'DietaryHabits']
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    
    # Process each row in the CSV
    for index, row in df.iterrows():
        try:
            # Insert into Patient table
            cursor.execute("""
                INSERT INTO Patient (PatientID, Age, Gender, Income)
                VALUES (?, ?, ?, ?)
            """, (
                row['PatientID'], 
                row['Age'] * 100,  # Scale age from 0-1 to 0-100
                row['Gender'], 
                row['Income'] * 100000  # Scale income
            ))
            
            # Insert into VitalSigns
            cursor.execute("""
                INSERT INTO VitalSigns (PatientID, SystolicBP, SystolicBP_Level, 
                                       HeartRate, DiastolicBP, DiastolicBP_Level, BMI, BMI_Level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['PatientID'],
                row['Systolic blood pressure'] * 200,  # Scale BP to realistic range
                row['SystolicBP_Level'],
                row['Heart rate'] * 200,  # Scale heart rate
                row['Diastolic blood pressure'] * 120,  # Scale diastolic BP
                row['DiastolicBP_Level'],
                row['BMI'],
                row['BMI_Level']
            ))
            
            # Insert into LabResults
            cursor.execute("""
                INSERT INTO LabResults (PatientID, Cholesterol, Cholesterol_Level,
                                      BloodSugar, BloodSugar_Level, Triglycerides,
                                      CK_MB, CK_MB_Level, Troponin, Troponin_Level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['PatientID'],
                row['Cholesterol'] * 300,  # Scale to realistic range
                row['CholesterolLevel'],
                row['Blood sugar'] * 300,  # Scale to realistic range
                row['BloodSugarLevel'],
                row['Triglycerides'] * 500,  # Scale to realistic range
                row['CK-MB'],
                row['CKMBLevel'],
                row['Troponin'],
                row['TroponinLevel']
            ))
            
            # Insert into Lifestyle
            cursor.execute("""
                INSERT INTO Lifestyle (PatientID, Smoking, AlcoholConsumption,
                                     ExerciseHoursPerWeek, Diet, SleepHoursPerDay,
                                     SedentaryHoursPerDay, Obesity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['PatientID'],
                row['Smoking'],
                row['Alcohol Consumption'],
                row['Exercise Hours Per Week'] * 10,  # Scale to realistic range
                row['Diet'],
                row['Sleep Hours Per Day'] * 10,  # Scale to realistic range
                row['Sedentary Hours Per Day'] * 16,  # Scale to realistic range
                row['Obesity']
            ))
            
            # Insert into MedicalHistory
            cursor.execute("""
                INSERT INTO MedicalHistory (PatientID, Diabetes, FamilyHistory,
                                          PreviousHeartProblems, MedicationUse)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['PatientID'],
                row['Diabetes'],
                row['Family History'],
                row['Previous Heart Problems'],
                row['Medication Use']
            ))
            
            # Insert into RiskAssessment
            risk_text = row['Heart Attack Risk (Text)']
            if not risk_text:  # Handle empty text
                risk_text = 'Low Risk' if row['Heart Attack Risk (Binary)'] == 0 else 'High Risk'
            
            cursor.execute("""
                INSERT INTO RiskAssessment (PatientID, StressLevel, StressLevel_Category,
                                          HeartAttackRiskBinary, HeartAttackRiskText)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['PatientID'],
                row['Stress Level'],
                row['StressLevelCategory'] if not pd.isna(row['StressLevelCategory']) else 
                    ('Low' if row['Stress Level'] < 3 else 
                     'Medium' if row['Stress Level'] < 7 else 'High'),
                row['Heart Attack Risk (Binary)'],
                risk_text
            ))
            
            # Insert into DietaryHabits
            diet_score = 5  # Default
            if not pd.isna(row['Diet']):
                if row['Diet'] == 0:
                    diet_type = 'Poor'
                    diet_score = 3
                elif row['Diet'] == 1:
                    diet_type = 'Average'
                    diet_score = 5
                else:
                    diet_type = 'Good'
                    diet_score = 8
            else:
                diet_type = 'Average'
            
            cursor.execute("""
                INSERT INTO DietaryHabits (PatientID, DietType, DietScore)
                VALUES (?, ?, ?)
            """, (
                row['PatientID'],
                diet_type,
                diet_score
            ))
            
            # Commit every 100 rows
            if index % 100 == 0:
                conn.commit()
                print(f"Processed {index} rows")
        
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    
    # Final commit
    conn.commit()
    print("Data import completed successfully")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    csv_path = "Heart Attack dataset.csv"
    db_path = "heart_risk_monitor/heart_risk_data.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    import_csv_to_sqlite(csv_path, db_path)
    print("CSV data has been imported to SQLite database successfully!")
