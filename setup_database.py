import sqlite3
import os

def setup_database():
    # Path to the database file
    db_path = 'heart_risk_monitor/heart_risk_data.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Read SQL script
    with open('Script-1.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    
    # Connect to new database and execute script
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql_script)
        conn.commit()
        print(f"Database created and populated successfully: {db_path}")
    except sqlite3.Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
