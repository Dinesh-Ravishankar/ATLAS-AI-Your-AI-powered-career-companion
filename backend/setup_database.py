"""
Database Migration Script for Supabase
Run this after configuring your Supabase connection to create all tables
"""

import sys
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.append(str(Path(__file__).parent))

from config import engine, settings
from models.database import Base, User, Profile, Skill, Project, user_skills
from sqlalchemy import inspect

def check_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful!")
            print(f"📍 Connected to: {settings.database_url.split('@')[1].split('/')[0]}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def list_existing_tables():
    """List all existing tables in the database"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print(f"\n📋 Existing tables ({len(tables)}):")
        for table in tables:
            print(f"   - {table}")
    else:
        print("\n📋 No existing tables found")
    return tables

def create_tables():
    """Create all tables defined in models"""
    try:
        print("\n🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def verify_tables():
    """Verify all expected tables exist"""
    expected_tables = ['users', 'profiles', 'skills', 'projects', 'user_skills']
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print("\n🔍 Verifying tables:")
    all_exist = True
    for table in expected_tables:
        if table in existing_tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("🚀 ATLAS AI - Supabase Database Setup")
    print("=" * 60)
    
    # Step 1: Check connection
    print("\n[Step 1/3] Testing database connection...")
    if not check_connection():
        print("\n⚠️  Please check your .env file and Supabase credentials")
        return
    
    # Step 2: List existing tables
    print("\n[Step 2/3] Checking existing tables...")
    list_existing_tables()
    
    # Step 3: Create tables
    print("\n[Step 3/3] Creating/updating database schema...")
    if create_tables():
        verify_tables()
        print("\n" + "=" * 60)
        print("✨ Database setup complete!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Visit your Supabase dashboard")
        print("   2. Go to 'Table Editor' to see your tables")
        print("   3. Start the API server: python main.py")
        print("   4. Test endpoints at: http://localhost:8000/docs")
    else:
        print("\n⚠️  Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    main()
