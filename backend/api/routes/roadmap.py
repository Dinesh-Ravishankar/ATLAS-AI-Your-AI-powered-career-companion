"""
Learning Roadmap API Routes
"""

from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from ai.roadmap_generator import roadmap_generator
from config import get_db
from models.database import User, Profile
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])


# Request/Response Models
class GenerateRoadmapRequest(BaseModel):
    career_goal: str = Field(..., description="Target career or skill")
    current_level: str = Field(default="beginner", description="beginner, intermediate, advanced")
    time_commitment: str = Field(default="moderate", description="light, moderate, intensive")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="Learning preferences")
    
    class Config:
        json_schema_extra = {
            "example": {
                "career_goal": "Data Scientist",
                "current_level": "beginner",
                "time_commitment": "moderate",
                "preferences": {
                    "learning_style": "mixed",
                    "budget": "free"
                }
            }
        }


class UpdateMilestoneRequest(BaseModel):
    roadmap: Dict[str, Any] = Field(..., description="Complete roadmap object")
    phase_number: int = Field(..., description="Phase number (1-indexed)")
    milestone_week: int = Field(..., description="Milestone week number")
    completed: bool = Field(..., description="Completion status")


class RoadmapResponse(BaseModel):
    success: bool
    roadmap: Dict[str, Any]
    message: Optional[str] = None


class ProgressResponse(BaseModel):
    success: bool
    progress: Dict[str, Any]


# Routes
# Routes
@router.get("/", response_model=RoadmapResponse)
async def get_user_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's roadmap. Generates one if it doesn't exist.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    if profile.roadmap:
        return RoadmapResponse(success=True, roadmap=profile.roadmap)
        
    # Generate default roadmap if none exists
    target_role = profile.target_roles[0] if profile.target_roles else "Full Stack Developer"
    
    try:
        roadmap = roadmap_generator.generate_roadmap(
            career_goal=target_role,
            current_level="beginner", # Default, could be inferred from profile
            time_commitment="moderate",
            preferences={}
        )
        
        # Save to profile
        profile.roadmap = roadmap
        db.commit()
        
        return RoadmapResponse(
            success=True, 
            roadmap=roadmap,
            message="Roadmap generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=RoadmapResponse)
async def generate_roadmap(
    request: GenerateRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate and SAVE a personalized learning roadmap
    """
    try:
        roadmap = roadmap_generator.generate_roadmap(
            career_goal=request.career_goal,
            current_level=request.current_level,
            time_commitment=request.time_commitment,
            preferences=request.preferences or {}
        )
        
        # Save to profile
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if profile:
            profile.roadmap = roadmap
            db.commit()
        
        return RoadmapResponse(
            success=True,
            roadmap=roadmap,
            message=f"Roadmap generated successfully for {request.career_goal}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate roadmap: {str(e)}"
        )


@router.post("/update-milestone")
async def update_milestone(
    request: UpdateMilestoneRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update milestone completion status in stored roadmap
    """
    try:
        # We ignore request.roadmap and use the stored one to ensure security/consistency
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if not profile or not profile.roadmap:
            raise HTTPException(status_code=404, detail="Roadmap not found")
            
        current_roadmap = dict(profile.roadmap) # Ensure it's a dict
        
        updated_roadmap = roadmap_generator.update_milestone(
            roadmap=current_roadmap,
            phase_number=request.phase_number,
            milestone_week=request.milestone_week,
            completed=request.completed
        )
        
        # Save updated roadmap
        profile.roadmap = updated_roadmap
        
        # Award XP if completed
        if request.completed:
            profile.xp = (profile.xp or 0) + 50
            
        db.commit()
        
        return RoadmapResponse(
            success=True,
            roadmap=updated_roadmap,
            message="Milestone updated successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update milestone: {str(e)}"
        )


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for stored roadmap
    """
    try:
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if not profile or not profile.roadmap:
            return ProgressResponse(success=True, progress={"percent_complete": 0, "completed_milestones": 0, "total_milestones": 0})
            
        progress = roadmap_generator.get_progress(profile.roadmap)
        
        return ProgressResponse(
            success=True,
            progress=progress
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate progress: {str(e)}"
        )


@router.get("/templates")
async def get_templates():
    """Get popular roadmap templates"""
    templates = [
        {
            "id": "fullstack_web",
            "title": "Full Stack Web Developer",
            "description": "Master frontend and backend development",
            "duration_weeks": 24,
            "level": "beginner",
            "popular": True
        },
        {
            "id": "data_scientist",
            "title": "Data Scientist",
            "description": "Learn data analysis, ML, and statistics",
            "duration_weeks": 28,
            "level": "beginner",
            "popular": True
        },
        {
            "id": "ml_engineer",
            "title": "Machine Learning Engineer",
            "description": "Build and deploy ML models",
            "duration_weeks": 32,
            "level": "intermediate",
            "popular": True
        },
        {
            "id": "cloud_architect",
            "title": "Cloud Solutions Architect",
            "description": "Design and implement cloud infrastructure",
            "duration_weeks": 20,
            "level": "intermediate",
            "popular": False
        },
        {
            "id": "devops_engineer",
            "title": "DevOps Engineer",
            "description": "CI/CD, automation, and infrastructure",
            "duration_weeks": 22,
            "level": "intermediate",
            "popular": False
        },
        {
            "id": "mobile_dev",
            "title": "Mobile App Developer",
            "description": "Build iOS and Android applications",
            "duration_weeks": 20,
            "level": "beginner",
            "popular": False
        }
    ]
    
    return {
        "success": True,
        "templates": templates
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "roadmap_generator",
        "version": "1.0.0"
    }
