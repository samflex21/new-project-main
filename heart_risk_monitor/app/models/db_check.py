import sqlite3
import os

def check_vital_signs_table():
    """
    Utility function to directly check the VitalSigns table in the database
    """
    db_path = 'C:/Users/samuel/Desktop/new-project-main/capstone2_project.db'
    
    # Check if file exists
    if not os.path.exists(db_path):
        return {"error": f"Database file not found at {db_path}"}
    
    conn = None
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if VitalSigns table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        
        results = {
            "tables": tables,
            "vital_signs_exists": "VitalSigns" in tables
        }
        
        if "VitalSigns" in tables:
            # Get column info
            cursor.execute("PRAGMA table_info(VitalSigns)")
            columns = cursor.fetchall()
            column_info = [{"name": col[1], "type": col[2]} for col in columns]
            
            # Get row count
            cursor.execute("SELECT COUNT(*) FROM VitalSigns")
            row_count = cursor.fetchone()[0]
            
            # Get sample data (first 3 rows)
            cursor.execute("SELECT * FROM VitalSigns LIMIT 3")
            sample_rows = cursor.fetchall()
            sample_data = []
            
            if sample_rows:
                for row in sample_rows:
                    sample_data.append(dict(row))
            
            results.update({
                "columns": column_info,
                "row_count": row_count,
                "sample_data": sample_data
            })
        
        return results
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print(check_vital_signs_table())
