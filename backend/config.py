from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: str = ""
    onet_api_key: str = ""
    github_token: str = ""
    esco_api_url: str = "https://ec.europa.eu/esco/api"
    environment: str = "development"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Database setup
# Use NullPool for Supabase Transaction Pooler (Port 6543) to avoid connection pooling issues
# This is recommended for serverless/transient connections
import os as _os

_use_sqlite = False

try:
    if "supabase.com" in settings.database_url:
        engine = create_engine(
            settings.database_url,
            poolclass=NullPool,
            connect_args={
                "connect_timeout": 15,  # 15 second connection timeout
            },
        )
    elif settings.database_url.startswith("sqlite"):
        engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(settings.database_url)
    
    # Quick connectivity test with timeout
    from sqlalchemy import text as _text
    with engine.connect() as conn:
        conn.execute(_text("SELECT 1"))
    print("✅ Database connected successfully")
except Exception as e:
    print(f"⚠️  Database connection failed ({type(e).__name__}: {e}), falling back to local SQLite")
    _use_sqlite = True

if _use_sqlite:
    _db_path = _os.path.join(_os.path.dirname(__file__), "atlas_ai.db")
    engine = create_engine(f"sqlite:///{_db_path}", connect_args={"check_same_thread": False})
    print(f"📁 Using local SQLite: {_db_path}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
