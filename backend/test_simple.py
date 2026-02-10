"""
Simple database connection test
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print("Testing database connection...")
print(f"Environment: {os.getenv('ENVIRONMENT')}")

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ Connected successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"\nPostgreSQL version:\n{version}")
    
    cursor.execute("SELECT current_database();")
    db = cursor.fetchone()[0]
    print(f"\nCurrent database: {db}")
    
    conn.close()
    print("\n✅ Connection test passed!")
    
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"Error: {e}")
    print("\nCheck DATABASE_CONNECTION_STEPS.md for troubleshooting")
