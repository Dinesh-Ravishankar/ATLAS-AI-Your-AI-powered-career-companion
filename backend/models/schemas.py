from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Profile Schemas
class ProfileBase(BaseModel):
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    major: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None
    preferences: Optional[dict] = {}  # User settings

class ProfileUpdate(ProfileBase):
    education: Optional[List[dict]] = None
    target_roles: Optional[List[str]] = None
    interests: Optional[List[str]] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    level: int
    xp: int
    badges: Optional[List[str]] = []
    education: Optional[List[dict]] = []
    target_roles: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    
    class Config:
        from_attributes = True

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = "technical"

class SkillCreate(SkillBase):
    proficiency: float = 0.5  # 0-1 scale

class SkillResponse(SkillBase):
    id: int
    esco_uri: Optional[str] = None
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    tech_stack: Optional[List[str]] = []

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Career Schemas
class CareerRecommendation(BaseModel):
    title: str
    match_score: float  # 0-100
    description: str
    required_skills: List[str]
    average_salary: Optional[float] = None
    growth_rate: Optional[float] = None
    reasons: List[str]  # Why this career was recommended

# Skill Gap Schemas
class SkillGapAnalysis(BaseModel):
    target_role: str
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[dict]  # [{name, priority, time_to_learn}]
    match_percentage: float
    recommendations: List[str]

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
