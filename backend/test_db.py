import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Attempting to connect to: {db_url}")

try:
    # Try with SSL required
    print("Testing connection with sslmode=require...")
    conn = psycopg2.connect(db_url, sslmode='require', connect_timeout=10)
    print("✅ Connected successfully with sslmode=require!")
    conn.close()
except Exception as e:
    print(f"❌ Failed with sslmode=require: {e}")
    
    try:
        # Try without explicit SSL
        print("Testing connection without explicit sslmode...")
        conn = psycopg2.connect(db_url, connect_timeout=10)
        print("✅ Connected successfully!")
        conn.close()
    except Exception as e2:
        print(f"❌ Failed without explicit sslmode: {e2}")

try:
    # Try direct port if it's the pooler
    if "6543" in db_url:
        direct_url = db_url.replace(":6543/", ":5432/")
        print(f"Testing direct connection (port 5432): {direct_url}")
        conn = psycopg2.connect(direct_url, sslmode='require', connect_timeout=10)
        print("✅ Connected successfully to port 5432!")
        conn.close()
except Exception as e3:
    print(f"❌ Direct connection failed: {e3}")
