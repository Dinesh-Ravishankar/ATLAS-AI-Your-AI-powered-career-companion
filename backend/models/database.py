from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from config import Base

# Association table for User-Skill many-to-many relationship
user_skills = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id')),
    Column('proficiency', Float, default=0.5),  # 0-1 scale
    Column('source', String, default='self')  # 'self', 'github', 'esco'
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    skills = relationship("Skill", secondary=user_skills, back_populates="users")
    projects = relationship("Project", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    # Basic Info
    bio = Column(String)
    location = Column(String)
    phone = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)
    
    # Academic
    education = Column(JSON)  # Array of education objects
    gpa = Column(Float)
    major = Column(String)
    university = Column(String)
    graduation_year = Column(Integer)
    
    # Career
    target_roles = Column(JSON)  # Array of target career paths
    interests = Column(JSON)  # Array of interest tags
    experience_years = Column(Float, default=0)
    
    # Gamification
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    badges = Column(JSON)  # Array of earned badges
    
    # Roadmap
    roadmap = Column(JSON)  # Stored roadmap object
    preferences = Column(JSON, default={})  # User settings (notifications, theme, etc.)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # 'technical', 'soft', 'domain'
    esco_uri = Column(String)  # Link to ESCO ontology
    description = Column(String)
    
    # Relationships
    users = relationship("User", secondary=user_skills, back_populates="skills")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    title = Column(String, nullable=False)
    description = Column(String)
    github_url = Column(String)
    live_url = Column(String)
    tech_stack = Column(JSON)  # Array of technologies
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")

class Career(Base):
    __tablename__ = "careers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    esco_uri = Column(String)
    onet_code = Column(String)
    description = Column(String)
    required_skills = Column(JSON)  # Array of skill names
    average_salary = Column(Float)
    growth_rate = Column(Float)  # Percentage
    work_life_balance_score = Column(Float)  # 0-10
    
class Scholarship(Base):
    __tablename__ = "scholarships"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String)
    amount = Column(Float)
    deadline = Column(DateTime)
    eligibility = Column(JSON)  # Array of criteria
    application_url = Column(String)
    description = Column(String)
    tags = Column(JSON)  # For matching (e.g., 'stem', 'underrepresented')
