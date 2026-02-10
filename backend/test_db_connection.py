"""
Database Connection Test Script
Tests the connection to Supabase PostgreSQL database
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import sys

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection and display detailed information"""
    
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Get DATABASE_URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        return False
    
    # Mask password for display
    masked_url = database_url
    if "@" in database_url:
        parts = database_url.split("@")
        if ":" in parts[0]:
            user_pass = parts[0].split(":")
            if len(user_pass) > 2:
                masked_url = f"{user_pass[0]}:{user_pass[1]}:****@{parts[1]}"
    
    print(f"\n📍 Database URL: {masked_url}")
    print(f"📍 Environment: {os.getenv('ENVIRONMENT', 'not set')}")
    
    # Test connection
    print("\n🔄 Testing connection...")
    
    try:
        # Create engine
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=False
        )
        
        # Test connection
        with engine.connect() as connection:
            # Execute a simple query
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            
            print("✅ Connection successful!")
            print(f"\n📊 PostgreSQL Version:")
            print(f"   {version}")
            
            # Get database name
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"\n📁 Current Database: {db_name}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"\n📋 Existing Tables ({len(tables)}):")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("\n⚠️  No tables found in database")
                print("   Run migrations to create tables:")
                print("   > alembic upgrade head")
            
            # Test write permission
            try:
                connection.execute(text("CREATE TEMP TABLE test_write (id INT);"))
                connection.execute(text("DROP TABLE test_write;"))
                print("\n✅ Write permissions: OK")
            except Exception as e:
                print(f"\n⚠️  Write permissions: Limited")
                print(f"   Error: {str(e)}")
            
            return True
            
    except OperationalError as e:
        print("❌ Connection failed!")
        print(f"\n🔍 Error Details:")
        print(f"   {str(e)}")
        
        # Common error suggestions
        print("\n💡 Troubleshooting:")
        if "password authentication failed" in str(e):
            print("   - Check your database password in .env")
            print("   - Verify password in Supabase Dashboard > Settings > Database")
        elif "could not translate host name" in str(e):
            print("   - Check your DATABASE_URL format")
            print("   - Verify project reference in Supabase Dashboard")
        elif "timeout" in str(e).lower():
            print("   - Check your internet connection")
            print("   - Verify Supabase project is active")
        else:
            print("   - Verify DATABASE_URL in .env file")
            print("   - Check Supabase Dashboard > Settings > Database")
            print("   - Ensure you're using the 'Transaction' pooling mode (port 6543)")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_supabase_config():
    """Test Supabase configuration"""
    
    print("\n" + "=" * 60)
    print("SUPABASE CONFIGURATION CHECK")
    print("=" * 60)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    checks = {
        "SUPABASE_URL": supabase_url,
        "SUPABASE_ANON_KEY": supabase_anon_key,
        "SUPABASE_SERVICE_KEY": supabase_service_key
    }
    
    all_set = True
    for key, value in checks.items():
        if value and not value.startswith("your-"):
            print(f"✅ {key}: Set")
        else:
            print(f"❌ {key}: Not configured")
            all_set = False
    
    if not all_set:
        print("\n💡 Get these values from:")
        print("   Supabase Dashboard > Project Settings > API")
    
    return all_set

if __name__ == "__main__":
    print("\n")
    
    # Test database connection
    db_ok = test_database_connection()
    
    # Test Supabase config
    supabase_ok = test_supabase_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if db_ok:
        print("✅ Database connection: SUCCESS")
    else:
        print("❌ Database connection: FAILED")
    
    if supabase_ok:
        print("✅ Supabase configuration: COMPLETE")
    else:
        print("⚠️  Supabase configuration: INCOMPLETE")
    
    print("\n")
    
    # Exit with appropriate code
    sys.exit(0 if db_ok else 1)
