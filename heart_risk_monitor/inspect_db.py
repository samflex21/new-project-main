"""
Inspect the SQLite database structure and sample data
"""
import sqlite3
import pandas as pd

# Connect to the database
db_path = "C:/Users/samuel/Desktop/new-project-main/capstone2_project.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")
print("\n")

# For each table, show its structure and sample data
for table_name in [t[0] for t in tables]:
    print(f"=== Table: {table_name} ===")
    
    # Get column info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Get sample data (first 5 rows)
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    rows = cursor.fetchall()
    if rows:
        print("\nSample data (first 5 rows):")
        for row in rows:
            print(f"  {row}")
    else:
        print("\nNo data in this table")
    
    print("\n" + "-"*50 + "\n")

conn.close()
print("Database inspection complete.")
