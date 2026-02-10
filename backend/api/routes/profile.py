from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from config import get_db
from models.database import User, Profile, Skill, Project, user_skills
from models.schemas import (
    ProfileResponse,
    ProfileUpdate,
    SkillCreate,
    SkillResponse,
    ProjectCreate,
    ProjectResponse
)
from auth.jwt_handler import get_current_user
from ai.resume_generator import export_resume_pdf

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/skills", response_model=SkillResponse)
def add_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if skill exists
    skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
    if not skill:
        skill = Skill(name=skill_data.name, category=skill_data.category)
        db.add(skill)
        db.commit()
        db.refresh(skill)
    
    # Add to user's skills
    stmt = user_skills.insert().values(
        user_id=current_user.id,
        skill_id=skill.id,
        proficiency=skill_data.proficiency,
        source='self'
    )
    db.execute(stmt)
    db.commit()
    
    return skill

@router.get("/skills", response_model=List[SkillResponse])
def get_user_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.skills

@router.delete("/skills/{skill_id}")
def remove_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = user_skills.delete().where(
        user_skills.c.user_id == current_user.id,
        user_skills.c.skill_id == skill_id
    )
    db.execute(stmt)
    db.commit()
    return {"message": "Skill removed successfully"}

@router.post("/projects", response_model=ProjectResponse)
def add_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = Project(**project_data.dict(), user_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/projects", response_model=List[ProjectResponse])
def get_user_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.projects

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.get("/export-resume")
def export_resume(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Export user's Atlas Card as a PDF resume"""
    # Get profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please complete your profile first.")
    
    # Prepare user data
    user_data = {
        'full_name': current_user.full_name or 'Your Name',
        'email': current_user.email
    }
    
    # Prepare profile data
    profile_data = {
        'bio': profile.bio,
        'location': profile.location,
        'phone': profile.phone,
        'linkedin_url': profile.linkedin_url,
        'github_url': profile.github_url,
        'portfolio_url': profile.portfolio_url,
        'major': profile.major,
        'university': profile.university,
        'graduation_year': profile.graduation_year,
        'gpa': profile.gpa,
        'education': profile.education or [],
        'target_roles': profile.target_roles or []
    }
    
    # Get skills
    skills = [{'name': skill.name, 'category': skill.category} for skill in current_user.skills]
    
    # Get projects
    projects = []
    for project in current_user.projects[:5]:  # Limit to 5 projects
        projects.append({
            'title': project.title,
            'description': project.description,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'tech_stack': project.tech_stack or []
        })
    
    # Generate PDF
    pdf_buffer = export_resume_pdf(user_data, profile_data, skills, projects)
    
    # Return PDF as streaming response
    filename = f"{current_user.full_name.replace(' ', '_')}_Resume.pdf" if current_user.full_name else "Atlas_Resume.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
