import os
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_database_data():
    # Path to the SQLite database
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        logging.error(f"Database file not found at {db_path}")
        return
    
    logging.info(f"Database file found at {db_path}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if tables exist
        tables_to_check = ['Patient', 'VitalSigns', 'LabResults']
        
        for table in tables_to_check:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                logging.info(f"Table {table} exists with {row_count} rows")
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                logging.info(f"Table {table} columns: {column_names}")
                
                # Get sample data
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample_rows = cursor.fetchall()
                for i, row in enumerate(sample_rows):
                    row_dict = {column: row[column] for column in column_names}
                    logging.info(f"Sample row {i+1} from {table}: {row_dict}")
            else:
                logging.error(f"Table {table} does not exist in the database")
        
        # Test a join query similar to what we're using in the application
        logging.info("Testing join query for patient metrics...")
        query = """
        SELECT 
            p.PatientID,
            p.weight,
            p.height,
            p.weight / ((p.height/100.0) * (p.height/100.0)) as bmi,
            v.SystolicBP,
            v.DiastolicBP,
            l.Cholesterol,
            l.BloodSugar
        FROM 
            Patient p
        LEFT JOIN 
            VitalSigns v ON p.PatientID = v.PatientID
        LEFT JOIN 
            LabResults l ON p.PatientID = l.PatientID
        LIMIT 5
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            logging.info(f"Found {len(results)} rows from join query")
            for i, row in enumerate(results):
                logging.info(f"Join result {i+1}: {dict(row)}")
                
                # Calculate the clinical values as we would in the application
                systolic = row['SystolicBP'] * 90 + 90 if row['SystolicBP'] is not None else None
                diastolic = row['DiastolicBP'] * 60 + 60 if row['DiastolicBP'] is not None else None
                cholesterol = row['Cholesterol'] * 150 + 150 if row['Cholesterol'] is not None else None
                blood_sugar = row['BloodSugar'] * 100 + 70 if row['BloodSugar'] is not None else None
                
                logging.info(f"Calculated clinical values: Systolic={systolic}, Diastolic={diastolic}, Cholesterol={cholesterol}, Blood Sugar={blood_sugar}")
        else:
            logging.error("No results found from join query")
        
        # Test population averages query
        logging.info("Testing population averages query...")
        pop_query = """
        SELECT 
            AVG(p.weight / ((p.height/100.0) * (p.height/100.0))) as avg_bmi,
            AVG(v.SystolicBP) as avg_systolic,
            AVG(v.DiastolicBP) as avg_diastolic,
            AVG(l.Cholesterol) as avg_cholesterol,
            AVG(l.BloodSugar) as avg_blood_sugar
        FROM 
            Patient p
        LEFT JOIN 
            VitalSigns v ON p.PatientID = v.PatientID
        LEFT JOIN 
            LabResults l ON p.PatientID = l.PatientID
        """
        
        cursor.execute(pop_query)
        pop_result = cursor.fetchone()
        
        if pop_result:
            logging.info(f"Population averages (raw): {dict(pop_result)}")
            
            # Calculate the clinical values
            avg_systolic = pop_result['avg_systolic'] * 90 + 90 if pop_result['avg_systolic'] is not None else None
            avg_diastolic = pop_result['avg_diastolic'] * 60 + 60 if pop_result['avg_diastolic'] is not None else None
            avg_cholesterol = pop_result['avg_cholesterol'] * 150 + 150 if pop_result['avg_cholesterol'] is not None else None
            avg_blood_sugar = pop_result['avg_blood_sugar'] * 100 + 70 if pop_result['avg_blood_sugar'] is not None else None
            
            logging.info(f"Population averages (clinical): BMI={pop_result['avg_bmi']}, Systolic={avg_systolic}, Diastolic={avg_diastolic}, Cholesterol={avg_cholesterol}, Blood Sugar={avg_blood_sugar}")
        else:
            logging.error("No population averages found")
        
    except Exception as e:
        logging.error(f"Error testing database: {e}")
        import traceback
        logging.error(traceback.format_exc())
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    logging.info("Starting database test...")
    test_database_data()
    logging.info("Database test complete")
