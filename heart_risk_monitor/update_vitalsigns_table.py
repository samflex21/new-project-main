import sqlite3
import pandas as pd
import os

def update_vitalsigns_with_recorddate():
    """
    Update the VitalSigns table in the SQLite database to include RecordDate from the CSV file.
    """
    # Paths
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    csv_path = 'C:/Users/samuel/Desktop/new-project-main/Heart Attack dataset.csv'
    
    # Check if files exist
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
        
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return False
    
    try:
        # Load CSV data
        print("Loading CSV data...")
        df = pd.read_csv(csv_path)
        
        # Check if RecordDate column exists
        if 'RecordDate' not in df.columns:
            print("RecordDate column not found in CSV file")
            return False
            
        # Connect to database
        print("Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if VitalSigns table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='VitalSigns'")
        if not cursor.fetchone():
            print("VitalSigns table does not exist in the database")
            conn.close()
            return False
            
        # Check if RecordDate column already exists in VitalSigns table
        cursor.execute("PRAGMA table_info(VitalSigns)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add RecordDate column if it doesn't exist
        if 'RecordDate' not in columns:
            print("Adding RecordDate column to VitalSigns table...")
            cursor.execute("ALTER TABLE VitalSigns ADD COLUMN RecordDate TEXT")
        else:
            print("RecordDate column already exists in VitalSigns table")
            
        # Get data mapping patient IDs to record dates
        patient_dates = df[['PatientID', 'RecordDate']].drop_duplicates()
        
        # Update VitalSigns table with RecordDate values
        print(f"Updating VitalSigns records with dates from CSV ({len(patient_dates)} patients)...")
        updated_count = 0
        
        for _, row in patient_dates.iterrows():
            patient_id = row['PatientID']
            record_date = row['RecordDate']
            
            cursor.execute(
                "UPDATE VitalSigns SET RecordDate = ? WHERE PatientID = ?", 
                (record_date, patient_id)
            )
            updated_count += cursor.rowcount
        
        # Commit changes
        conn.commit()
        print(f"Updated {updated_count} records in VitalSigns table")
        
        # Verify update
        cursor.execute("SELECT COUNT(*) FROM VitalSigns WHERE RecordDate IS NOT NULL")
        records_with_dates = cursor.fetchone()[0]
        print(f"Records with dates: {records_with_dates}")
        
        # Create index on RecordDate for better performance
        print("Creating index on RecordDate column...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vitalsigns_recorddate ON VitalSigns(RecordDate)")
        conn.commit()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating database: {e}")
        if 'conn' in locals() and conn:
            conn.close()
        return False

if __name__ == "__main__":
    success = update_vitalsigns_with_recorddate()
    if success:
        print("Successfully updated VitalSigns table with RecordDate")
    else:
        print("Failed to update VitalSigns table")
