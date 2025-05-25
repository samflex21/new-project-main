import sqlite3
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Database path
db_path = os.path.join(os.path.dirname(current_dir), 'capstone2_project.db')
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("\nTables in database:")
    for table in tables:
        print(f" - {table[0]}")
    
    # Check for LabResults table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LabResults'")
    if cursor.fetchone():
        print("\nLabResults table exists!")
        
        # Get column names
        cursor.execute("PRAGMA table_info(LabResults)")
        columns = cursor.fetchall()
        print("\nColumns in LabResults table:")
        for col in columns:
            print(f" - {col[1]} (Type: {col[2]})")
        
        # Get sample data
        cursor.execute("SELECT * FROM LabResults LIMIT 1")
        sample = cursor.fetchone()
        if sample:
            print("\nSample data from LabResults:")
            for i, col in enumerate(columns):
                print(f" - {col[1]}: {sample[i]}")
    else:
        print("\nLabResults table does not exist!")
        
        # Let's check for a table that might contain lab results
        print("\nLooking for tables that might contain lab data...")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            table_cols = [col[1] for col in cursor.fetchall()]
            
            # Check for common lab test columns
            lab_indicators = ['cholesterol', 'blood', 'sugar', 'glucose', 'triglyceride', 'ck', 'troponin', 'lab']
            matches = [col for col in table_cols if any(ind.lower() in col.lower() for ind in lab_indicators)]
            
            if matches:
                print(f"\nTable {table_name} might contain lab data with columns:")
                for match in matches:
                    print(f" - {match}")
    
    conn.close()
    
except Exception as e:
    print(f"Error accessing database: {str(e)}")
