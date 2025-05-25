import sqlite3
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_patient_metrics_comparison(patient_id=None):
    """
    Get patient metrics comparison data from the SQLite database.
    Compares a specific patient's metrics with the population average.
    
    Args:
        patient_id: Optional patient ID to filter data for a specific patient
        
    Returns:
        Dictionary with patient data and population averages
    """
    # Path to the SQLite database
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    
    # Default return structure with mock data as fallback
    default_data = {
        'labels': ['BMI', 'Systolic BP', 'Diastolic BP', 'Cholesterol', 'Blood Sugar'],
        'patient_data': [28, 138, 90, 220, 110],
        'population_data': [25, 120, 80, 190, 100],
        'is_mock_data': True
    }
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        logging.error(f"Database file not found at {db_path}")
        return default_data
    else:
        logging.info(f"Database file found at {db_path}")
    
    conn = None
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if necessary tables exist and their content
        required_tables = ['Patient', 'VitalSigns', 'LabResults']
        for table in required_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                logging.error(f"{table} table does not exist in the database")
                return default_data
            # Check table row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            logging.info(f"Table {table} exists with {row_count} rows")
            
            # Check schema of each table
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            logging.info(f"Table {table} columns: {column_names}")
        
        # First, check for actual sample values to understand the data scales
        logging.info("Checking sample data to understand scales...")
        cursor.execute("SELECT height, weight FROM Patient WHERE height > 0 AND weight > 0 LIMIT 5")
        sample_hw = cursor.fetchall()
        for i, row in enumerate(sample_hw):
            logging.info(f"Sample {i+1}: height={row['height']}, weight={row['weight']}")
            
        cursor.execute("SELECT SystolicBP, DiastolicBP, HeartRate FROM VitalSigns LIMIT 5")
        sample_vitals = cursor.fetchall()
        for i, row in enumerate(sample_vitals):
            logging.info(f"Sample {i+1}: SystolicBP={row['SystolicBP']}, DiastolicBP={row['DiastolicBP']}, HeartRate={row['HeartRate']}")
            
        cursor.execute("SELECT Cholesterol, BloodSugar FROM LabResults LIMIT 5")
        sample_labs = cursor.fetchall()
        for i, row in enumerate(sample_labs):
            logging.info(f"Sample {i+1}: Cholesterol={row['Cholesterol']}, BloodSugar={row['BloodSugar']}")
        
        # Query to get population averages
        population_query = """
        SELECT 
            AVG(v.BMI) as avg_bmi_raw,
            AVG(v.SystolicBP) as avg_systolic_raw,
            AVG(v.DiastolicBP) as avg_diastolic_raw,
            AVG(l.Cholesterol) as avg_cholesterol_raw,
            AVG(l.BloodSugar) as avg_blood_sugar_raw
        FROM 
            Patient p
        LEFT JOIN 
            VitalSigns v ON p.patient_ID = v.PatientID
        LEFT JOIN 
            LabResults l ON p.patient_ID = l.PatientID
        """
        
        cursor.execute(population_query)
        population_result = cursor.fetchone()
        
        if not population_result:
            logging.error("No population data found")
            return default_data
        
        logging.info(f"Raw population result: {dict(population_result)}")
        
        # Extract and scale population data from raw values
        # BMI is already normalized in the database (0-1 scale)
        raw_bmi = population_result['avg_bmi_raw']
        pop_bmi = round(raw_bmi * 30 + 15) if raw_bmi is not None else 25  # Scale BMI from 0-1 to 15-45 range
        
        # Scale the normalized vital signs and lab values to real clinical values
        # Get raw values first
        raw_systolic = population_result['avg_systolic_raw']
        raw_diastolic = population_result['avg_diastolic_raw']
        raw_cholesterol = population_result['avg_cholesterol_raw']
        raw_blood_sugar = population_result['avg_blood_sugar_raw']
        
        logging.info(f"Raw population values: Systolic={raw_systolic}, Diastolic={raw_diastolic}, Cholesterol={raw_cholesterol}, Blood Sugar={raw_blood_sugar}")
        
        # Convert normalized values (0-1) to actual clinical values
        pop_systolic = round(raw_systolic * 90 + 90) if raw_systolic is not None else 120  # 90-180 mmHg range
        pop_diastolic = round(raw_diastolic * 60 + 60) if raw_diastolic is not None else 80  # 60-120 mmHg range
        pop_cholesterol = round(raw_cholesterol * 150 + 150) if raw_cholesterol is not None else 190  # 150-300 mg/dL range
        pop_blood_sugar = round(raw_blood_sugar * 100 + 70) if raw_blood_sugar is not None else 100  # 70-170 mg/dL range
        
        logging.info(f"Population values after processing: BMI={pop_bmi}, Systolic={pop_systolic}, Diastolic={pop_diastolic}, Cholesterol={pop_cholesterol}, Blood Sugar={pop_blood_sugar}")
        
        population_data = [pop_bmi, pop_systolic, pop_diastolic, pop_cholesterol, pop_blood_sugar]
        logging.info(f"Population data: {population_data}")
        
        # Default patient data (will be overwritten if patient_id is provided)
        patient_data = population_data.copy()
        
        # If a specific patient is selected, get their data
        if patient_id:
            patient_query = """
            SELECT 
                v.BMI as bmi_raw,
                v.SystolicBP as systolic_raw,
                v.DiastolicBP as diastolic_raw,
                l.Cholesterol as cholesterol_raw,
                l.BloodSugar as blood_sugar_raw
            FROM 
                Patient p
            LEFT JOIN 
                VitalSigns v ON p.patient_ID = v.PatientID
            LEFT JOIN 
                LabResults l ON p.patient_ID = l.PatientID
            WHERE 
                p.patient_ID = ?
            LIMIT 1
            """
            
            cursor.execute(patient_query, (patient_id,))
            patient_result = cursor.fetchone()
            
            if patient_result:
                logging.info(f"Raw patient data: {dict(patient_result)}")
                
                # Extract and scale patient data from raw values
                # BMI is already normalized in the database (0-1 scale)
                raw_bmi = patient_result['bmi_raw']
                patient_bmi = round(raw_bmi * 30 + 15) if raw_bmi is not None else pop_bmi  # Scale BMI from 0-1 to 15-45 range
                
                # Get raw values
                raw_systolic = patient_result['systolic_raw']
                raw_diastolic = patient_result['diastolic_raw']
                raw_cholesterol = patient_result['cholesterol_raw']
                raw_blood_sugar = patient_result['blood_sugar_raw']
                
                # Convert normalized values (0-1) to actual clinical values
                patient_systolic = round(raw_systolic * 90 + 90) if raw_systolic is not None else pop_systolic  # 90-180 mmHg
                patient_diastolic = round(raw_diastolic * 60 + 60) if raw_diastolic is not None else pop_diastolic  # 60-120 mmHg
                patient_cholesterol = round(raw_cholesterol * 150 + 150) if raw_cholesterol is not None else pop_cholesterol  # 150-300 mg/dL
                patient_blood_sugar = round(raw_blood_sugar * 100 + 70) if raw_blood_sugar is not None else pop_blood_sugar  # 70-170 mg/dL
                
                patient_data = [patient_bmi, patient_systolic, patient_diastolic, patient_cholesterol, patient_blood_sugar]
                logging.info(f"Patient data for ID {patient_id} after processing: {patient_data}")
            else:
                logging.warning(f"No data found for patient ID {patient_id}")
        
        # Return the comparison data
        return {
            'labels': ['BMI', 'Systolic BP', 'Diastolic BP', 'Cholesterol', 'Blood Sugar'],
            'patient_data': patient_data,
            'population_data': population_data,
            'is_mock_data': False
        }
        
    except Exception as e:
        logging.error(f"Error getting patient metrics comparison: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return default_data
    finally:
        if conn:
            conn.close()
