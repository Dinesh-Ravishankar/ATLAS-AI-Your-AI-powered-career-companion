"""
Create all database tables directly using SQLAlchemy
Run this once to initialize your database schema
"""
from config import engine, Base
from models.database import User, Profile, Skill, Project, Career, Scholarship

print("Creating database tables...")

try:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    
    # List created tables
    print("\n📋 Created tables:")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")
        
except Exception as e:
    print(f"❌ Error creating tables: {e}")
