from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, profile, career
from api.routes import onboarding, skills
from api.routes import coach, origin_story, guide, roadmap
from models.database import Base
from config import engine

# Create database tables (gracefully handle connection issues)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")
except Exception as e:
    print(f"⚠️  Table creation skipped: {type(e).__name__}: {e}")

app = FastAPI(
    title="ATLAS AI API",
    description="AI-Powered Career Guidance Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(onboarding.router, prefix="/api")
app.include_router(skills.router, prefix="/api")
app.include_router(coach.router, prefix="/api")
app.include_router(origin_story.router, prefix="/api")
app.include_router(guide.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Welcome to ATLAS AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
