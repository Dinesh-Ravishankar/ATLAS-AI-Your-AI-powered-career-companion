"""
Onboarding Routes
Guided onboarding wizard for new users
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from config import get_db
from models.database import User, Profile, Skill, user_skills
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


class OnboardingStep1(BaseModel):
    """Basic info"""
    full_name: str
    major: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None


class OnboardingStep2(BaseModel):
    """Interests and goals"""
    interests: List[str] = []
    target_roles: List[str] = []


class OnboardingStep3(BaseModel):
    """Skills"""
    skills: List[str] = []


class OnboardingComplete(BaseModel):
    """Full onboarding data"""
    full_name: str
    major: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    interests: List[str] = []
    target_roles: List[str] = []
    skills: List[str] = []
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None


@router.get("/status")
def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if user has completed onboarding"""
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        return {"completed": False, "step": 0}

    step = 0
    if current_user.full_name:
        step = 1
    if profile.interests and len(profile.interests) > 0:
        step = 2
    if len(current_user.skills) > 0:
        step = 3

    completed = step >= 3
    return {"completed": completed, "step": step}


@router.post("/complete")
def complete_onboarding(
    data: OnboardingComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Complete full onboarding in one step"""
    # Update user name
    current_user.full_name = data.full_name
    db.add(current_user)

    # Update or create profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        db.flush()

    profile.major = data.major
    profile.university = data.university
    profile.graduation_year = data.graduation_year
    profile.interests = data.interests
    profile.target_roles = data.target_roles
    profile.bio = data.bio
    profile.github_url = data.github_url
    profile.linkedin_url = data.linkedin_url

    # Award onboarding XP
    profile.xp = (profile.xp or 0) + 300
    if profile.xp >= 200:
        profile.level = max(profile.level or 1, 2)

    # Add skills
    for skill_name in data.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name, category="technical")
            db.add(skill)
            db.flush()

        # Check if association already exists
        existing = db.execute(
            user_skills.select().where(
                user_skills.c.user_id == current_user.id,
                user_skills.c.skill_id == skill.id,
            )
        ).first()
        if not existing:
            db.execute(
                user_skills.insert().values(
                    user_id=current_user.id,
                    skill_id=skill.id,
                    proficiency=0.5,
                    source="onboarding",
                )
            )

    db.commit()

    return {
        "message": "Onboarding complete! Welcome to Atlas AI.",
        "xp_earned": 300,
        "level": profile.level,
    }


@router.post("/step1")
def onboarding_step1(
    data: OnboardingStep1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Step 1: Basic info"""
    current_user.full_name = data.full_name
    db.add(current_user)

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    profile.major = data.major
    profile.university = data.university
    profile.graduation_year = data.graduation_year

    db.commit()
    return {"message": "Step 1 complete", "step": 1}


@router.post("/step2")
def onboarding_step2(
    data: OnboardingStep2,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Step 2: Interests and goals"""
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Complete step 1 first")

    profile.interests = data.interests
    profile.target_roles = data.target_roles

    db.commit()
    return {"message": "Step 2 complete", "step": 2}


@router.post("/step3")
def onboarding_step3(
    data: OnboardingStep3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Step 3: Skills"""
    for skill_name in data.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name, category="technical")
            db.add(skill)
            db.flush()

        existing = db.execute(
            user_skills.select().where(
                user_skills.c.user_id == current_user.id,
                user_skills.c.skill_id == skill.id,
            )
        ).first()
        if not existing:
            db.execute(
                user_skills.insert().values(
                    user_id=current_user.id,
                    skill_id=skill.id,
                    proficiency=0.5,
                    source="onboarding",
                )
            )

    # Award XP
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 300
        if profile.xp >= 200:
            profile.level = max(profile.level or 1, 2)

    db.commit()
    return {"message": "Onboarding complete!", "step": 3, "xp_earned": 300}
