import sqlite3
import os
from fastapi import FastAPI

app = FastAPI()

# Find exactly where our database file is
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'backend', 'database.sqlite3')

# A helper function to open the bridge to our database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    # It tells SQLite to return data as Python Dictionaries 
    # instead of plain lists. So we get {"revenue": 500} instead of just [500]
    conn.row_factory = sqlite3.Row
    return conn


# --- FIRST ENDPOINT ---
@app.get("/api/summary")
def get_summary():
    # Open the connection and get our robot (cursor)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Write our SQL query
    query = """
        SELECT 
            SUM(net_revenue_usd) AS total_net_revenue,
            SUM(units_sold) AS total_units
        FROM sales
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the result (since we are just SUMming everything, there is only 1 row)
    row = cursor.fetchone()
    
    # Close the bridge
    conn.close()
    
    # Send the result back to the user as a JSON Dictionary
    return dict(row)