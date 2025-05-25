import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_vital_signs_timeline(patient_id=None):
    """
    Get vital signs timeline data from the SQLite database using RecordDate
    
    Args:
        patient_id: Optional patient ID to filter data for a specific patient
        
    Returns:
        Dictionary with vital signs timeline data including dates, systolic, diastolic, and heart rate values
    """
    # Path to the SQLite database
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    conn = None
    
    # Generate sample data for the timeline as fallback
    def generate_sample_data():
        # Create monthly dates for the past 6 months
        dates = []
        current_date = datetime.now()
        
        for i in range(5, -1, -1):
            past_date = current_date - relativedelta(months=i)
            dates.append(past_date.strftime('%b %Y'))
        
        logging.warning("Using mock vital signs data instead of database data")
        return {
            'dates': dates,
            'systolic': [120, 122, 125, 123, 128, 130],
            'diastolic': [80, 82, 83, 81, 85, 87],
            'heart_rate': [72, 75, 74, 76, 78, 80],
            'is_mock_data': True  # Flag to indicate mock data
        }
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        logging.error(f"Database file not found at {db_path}")
        return generate_sample_data()
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if VitalSigns table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='VitalSigns'")
        if not cursor.fetchone():
            logging.error("VitalSigns table does not exist in the database")
            return generate_sample_data()
        
        # Check if RecordDate column exists
        cursor.execute("PRAGMA table_info(VitalSigns)")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]
        
        logging.info(f"VitalSigns table columns: {columns}")
        
        if 'RecordDate' not in columns:
            logging.error("RecordDate column not found in VitalSigns table")
            return generate_sample_data()
        
        # Query to get vital signs data grouped by month
        query = """
        SELECT 
            strftime('%Y-%m', RecordDate) as month,
            AVG(SystolicBP * 90 + 90) as avg_systolic,
            AVG(DiastolicBP * 60 + 60) as avg_diastolic,
            AVG(HeartRate * 40 + 60) as avg_heart_rate
        FROM 
            VitalSigns
        WHERE
            RecordDate IS NOT NULL
        """
        
        # Add patient filter if needed
        params = ()
        if patient_id:
            query += " AND PatientID = ? "
            params = (patient_id,)
        
        # Group by month and order by date
        query += """
        GROUP BY month
        ORDER BY month
        LIMIT 6
        """
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if not results:
            logging.error("No vital signs data found with valid dates")
            return generate_sample_data()
        
        # Process results
        dates = []
        systolic = []
        diastolic = []
        heart_rate = []
        
        for row in results:
            # Convert YYYY-MM to a more readable format (e.g., Jan 2022)
            try:
                month_year = datetime.strptime(row['month'], '%Y-%m')
                formatted_date = month_year.strftime('%b %Y')
                dates.append(formatted_date)
            except ValueError:
                # Fallback if parsing fails
                dates.append(row['month'])
            
            # The values are already scaled in the SQL query
            systolic.append(round(row['avg_systolic']))
            diastolic.append(round(row['avg_diastolic']))
            heart_rate.append(round(row['avg_heart_rate']))
        
        # Debug output
        logging.info(f"Found {len(dates)} months of vital signs data from database")
        logging.info(f"Dates: {dates}")
        logging.info(f"Systolic: {systolic}")
        logging.info(f"Diastolic: {diastolic}")
        logging.info(f"Heart Rate: {heart_rate}")
        
        return {
            'dates': dates,
            'systolic': systolic,
            'diastolic': diastolic,
            'heart_rate': heart_rate,
            'is_mock_data': False  # Flag to indicate real database data
        }
    
    except Exception as e:
        logging.error(f"Error processing vital signs data from database: {e}")
        # Get detailed error information
        import traceback
        logging.error(traceback.format_exc())
        return generate_sample_data()
    finally:
        if conn:
            conn.close()
