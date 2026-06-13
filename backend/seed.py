import sqlite3
import pandas as pd
import os

# Define the paths so Python knows exactly where to find the files
# BASE_DIR gets the folder above the 'backend' folder (the main project folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'novabite_sales_data.csv')
DB_PATH = os.path.join(BASE_DIR, 'backend', 'database.sqlite3')

def seed_database():
    print(f"Reading CSV from: {CSV_PATH}")
    try:
        # 1. Read the CSV file
        df = pd.read_csv(CSV_PATH)
        
        # 2. Connect to SQLite (this automatically creates the file if it doesn't exist!)
        conn = sqlite3.connect(DB_PATH)
        
        # 3. Push the data into a table named 'sales'
        # if_exists='replace' means we can run this script multiple times safely
        df.to_sql('sales', conn, if_exists='replace', index=False)
        
        print("Successfully created the database!")
        
        # Let's verify it worked by asking the database how many rows it has
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        count = cursor.fetchone()[0]
        print(f"Total rows inserted: {count}")
        
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {CSV_PATH}")
    finally:
        # Always close the database connection when done
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    seed_database()