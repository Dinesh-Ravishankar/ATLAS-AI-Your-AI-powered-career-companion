from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from config import get_db
from models.database import User
from models.schemas import SkillGapAnalysis, CareerRecommendation
from auth.jwt_handler import get_current_user
from ai.skill_gap_analyzer import SkillGapAnalyzer
from ai.career_recommender import CareerRecommender
from ai.orchestrator import chat_with_counselor, get_ai_career_recommendations, CareerCounselorOrchestrator
from ai.ghost_job_detector import verify_job_posting
from ai.project_recommender import get_project_recommendations

router = APIRouter(prefix="/career", tags=["Career Guidance"])

skill_gap_analyzer = SkillGapAnalyzer()
career_recommender = CareerRecommender()
orchestrator = CareerCounselorOrchestrator()

# Request/Response Models
class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict]] = []


class ChatResponse(BaseModel):
    response: str
    timestamp: str


class JobPostingVerification(BaseModel):
    title: str
    description: str
    salary: Optional[str] = ""
    company: str
    company_verified: bool = False
    post_date: Optional[str] = None
    url: Optional[str] = None


class ProjectRecommendationRequest(BaseModel):
    target_role: str
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    count: int = 5


class ScholarshipRequest(BaseModel):
    major: Optional[str] = None
    location: Optional[str] = ""


class SideHustleRequest(BaseModel):
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class LearningPathRequest(BaseModel):
    target_role: str
    weekly_hours: int = 10


class MockInterviewRequest(BaseModel):
    role: str
    question_count: int = 5
    difficulty: str = "medium"  # easy, medium, hard


class CareerCompareRequest(BaseModel):
    careers: List[str]  # 2-3 career titles to compare

@router.post("/skill-gap", response_model=SkillGapAnalysis)
def analyze_skill_gap(
    target_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze skill gap between user's current skills and target role requirements"""
    # Get user's skills
    user_skills = [skill.name for skill in current_user.skills]
    
    if not user_skills:
        raise HTTPException(status_code=400, detail="Please add skills to your profile first")
    
    # Perform gap analysis
    analysis = skill_gap_analyzer.analyze_gap(user_skills, target_role)
    return analysis

@router.get("/recommendations", response_model=List[CareerRecommendation])
def get_career_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized career recommendations based on user profile"""
    # Get user data
    user_skills = [skill.name for skill in current_user.skills]
    profile = current_user.profile
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    interests = profile.interests or []
    gpa = profile.gpa or 3.0
    
    # Get recommendations
    recommendations = career_recommender.recommend(user_skills, interests, gpa)
    return recommendations

@router.post("/roadmap")
def get_career_roadmap(
    target_role: str,
    current_user: User = Depends(get_current_user)
):
    """Generate a step-by-step career roadmap"""
    user_skills = [skill.name for skill in current_user.skills]
    roadmap_json = orchestrator.generate_career_roadmap(target_role, user_skills)
    
    # Try to parse JSON if AI returned it as markdown
    try:
        import re
        json_match = re.search(r'\[.*\]', roadmap_json, re.DOTALL)
        if json_match:
            import json
            return json.loads(json_match.group())
        return roadmap_json
    except:
        return roadmap_json

@router.get("/trending-skills")
def get_trending_skills():
    """Get trending skills in the job market (mock data for demo)"""
    return {
        "trending": [
            {"name": "Generative AI", "growth": 250, "trend": "rising"},
            {"name": "Python", "growth": 45, "trend": "stable"},
            {"name": "Cloud Computing", "growth": 80, "trend": "rising"},
            {"name": "Data Analysis", "growth": 60, "trend": "stable"},
            {"name": "React", "growth": 35, "trend": "stable"}
        ],
        "declining": [
            {"name": "jQuery", "growth": -15, "trend": "declining"},
            {"name": "Flash", "growth": -90, "trend": "declining"}
        ]
    }


@router.post("/chat", response_model=ChatResponse)
def chat_with_ai_counselor(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with Atlas AI career counselor (powered by OpenAI + LangChain)"""
    from datetime import datetime
    
    # Build Atlas Card context
    atlas_card = {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "skills": [skill.name for skill in current_user.skills]
    }
    
    # Add profile data if available
    if current_user.profile:
        profile = current_user.profile
        atlas_card.update({
            "major": profile.major,
            "university": profile.university,
            "graduation_year": profile.graduation_year,
            "interests": profile.interests or [],
            "target_roles": profile.target_roles or []
        })
    
    # Get AI response
    try:
        response = chat_with_counselor(
            chat_request.message, 
            atlas_card, 
            chat_request.history
        )
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        # Fallback response if AI fails
        return ChatResponse(
            response="I'm having trouble connecting right now. Please try asking about your career path, skill gaps, or job search strategy!",
            timestamp=datetime.now().isoformat()
        )


@router.post("/recommendations-ai", response_model=List[Dict])
def get_ai_recommendations(
    preferences: Optional[Dict] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered career recommendations (uses OpenAI)"""
    # Build Atlas Card context
    atlas_card = {
        "full_name": current_user.full_name,
        "skills": [skill.name for skill in current_user.skills]
    }
    
    if current_user.profile:
        profile = current_user.profile
        atlas_card.update({
            "major": profile.major,
            "university": profile.university,
            "interests": profile.interests or [],
            "target_roles": profile.target_roles or []
        })
    
    # Get AI recommendations
    recommendations = get_ai_career_recommendations(atlas_card, preferences)
    return recommendations


@router.post("/verify-job")
def verify_job(
    job_data: JobPostingVerification,
    current_user: User = Depends(get_current_user)
):
    """Verify job posting and detect ghost jobs/scams"""
    analysis = verify_job_posting(job_data.dict())
    return analysis


@router.post("/project-recommendations")
def recommend_projects(
    request: ProjectRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project recommendations based on skills and target role"""
    # Get user skills
    user_skills = [skill.name for skill in current_user.skills]
    
    if not user_skills:
        user_skills = ["Programming"]  # Default fallback
    
    # Get recommendations
    projects = get_project_recommendations(
        skills=user_skills,
        target_role=request.target_role,
        difficulty=request.difficulty,
        count=request.count
    )
    
    return {"projects": projects, "count": len(projects)}


@router.post("/scholarships")
def get_scholarships(
    request: ScholarshipRequest,
    current_user: User = Depends(get_current_user)
):
    """Find scholarships and financial aid"""
    major = request.major or (current_user.profile.major if current_user.profile else "General")
    location = request.location or (current_user.profile.location if current_user.profile else "Global")
    
    raw_result = orchestrator.get_scholarships(major, location)
    # Ensure result is wrapped in object with 'scholarships' key
    if isinstance(raw_result, list):
        return {"scholarships": raw_result}
    return raw_result


@router.post("/side-hustles")
def get_side_hustles(
    request: SideHustleRequest,
    current_user: User = Depends(get_current_user)
):
    """Incubate side hustle ideas"""
    skills = request.skills or [skill.name for skill in current_user.skills]
    interests = request.interests or (current_user.profile.interests if current_user.profile else ["Technology"])
    
    if not skills:
        skills = ["Communication", "Basic Tech"]
    
    raw_result = orchestrator.get_side_hustle_ideas(skills, interests)
    # Ensure result is wrapped in object with 'side_hustles' key
    if isinstance(raw_result, list):
        return {"side_hustles": raw_result}
    return raw_result


@router.post("/learning-path")
def get_learning_path(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a personalized learning path for a target role"""
    from ai.learning_pathway import generate_learning_path

    user_skills_list = [skill.name for skill in current_user.skills]
    profile = current_user.profile

    # Get skill gap first to find missing skills
    analysis = skill_gap_analyzer.analyze_gap(user_skills_list, request.target_role)
    try:
        raw_missing = analysis.missing_skills if hasattr(analysis, 'missing_skills') else (analysis.get("missing_skills", []) if isinstance(analysis, dict) else [])
        missing = [s["name"] if isinstance(s, dict) else s for s in raw_missing]
    except Exception:
        missing = []

    if not missing:
        missing = ["Advanced " + request.target_role]

    current_level = "beginner"
    if profile and profile.experience_years:
        if profile.experience_years >= 3:
            current_level = "advanced"
        elif profile.experience_years >= 1:
            current_level = "intermediate"

    path = generate_learning_path(
        missing_skills=missing,
        target_role=request.target_role,
        current_level=current_level,
        weekly_hours=request.weekly_hours,
    )
    return {"target_role": request.target_role, "learning_path": path, "total_steps": len(path)}


@router.post("/mock-interview")
def mock_interview(
    request: MockInterviewRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate mock interview questions and evaluate answers"""
    from openai import OpenAI
    from config import get_settings
    import json, re

    settings = get_settings()

    user_skills_list = [skill.name for skill in current_user.skills]
    prompt = f"""Generate {request.question_count} mock interview questions for a {request.role} position.
Difficulty: {request.difficulty}
Candidate skills: {', '.join(user_skills_list[:10])}

Return ONLY a JSON array:
[
  {{
    "question": "Interview question text",
    "type": "behavioral/technical/situational",
    "tip": "Brief tip for answering well",
    "sample_answer": "A strong sample answer in 2-3 sentences"
  }}
]"""

    if not settings.openai_api_key:
        return {
            "role": request.role,
            "questions": [
                {
                    "question": f"Tell me about a time you used {user_skills_list[0] if user_skills_list else 'problem-solving'} to overcome a challenge.",
                    "type": "behavioral",
                    "tip": "Use the STAR method: Situation, Task, Action, Result",
                    "sample_answer": "In my previous project, I identified a performance bottleneck and used systematic debugging to resolve it, improving response times by 40%.",
                },
                {
                    "question": f"How would you approach learning a new technology required for this {request.role} role?",
                    "type": "situational",
                    "tip": "Show a structured approach to learning",
                    "sample_answer": "I would start by reading the official documentation, then build a small project to gain hands-on experience, and seek mentorship from experienced practitioners.",
                },
            ],
        }

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional career coach. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        questions = json.loads(json_match.group()) if json_match else json.loads(content)
        return {"role": request.role, "questions": questions}
    except Exception as e:
        print(f"Mock interview AI error: {e}")
        return {
            "role": request.role,
            "questions": [
                {"question": f"Tell me about a time you used {user_skills_list[0] if user_skills_list else 'problem-solving'} to overcome a challenge.", "type": "behavioral", "tip": "Use the STAR method: Situation, Task, Action, Result", "sample_answer": "In my previous project, I identified a performance bottleneck and used systematic debugging to resolve it, improving response times by 40%."},
                {"question": f"How would you approach learning a new technology required for this {request.role} role?", "type": "situational", "tip": "Show a structured approach to learning", "sample_answer": "I would start by reading the official documentation, then build a small project to gain hands-on experience, and seek mentorship from experienced practitioners."},
                {"question": "What is your greatest professional strength and how has it helped you succeed?", "type": "behavioral", "tip": "Be specific with examples and results", "sample_answer": "My greatest strength is analytical thinking. In my last project, I broke down a complex problem into smaller components, which helped the team deliver 2 weeks ahead of schedule."},
                {"question": f"Describe a project where you demonstrated skills relevant to {request.role}.", "type": "technical", "tip": "Focus on your role, technologies used, and measurable outcomes", "sample_answer": "I built a full-stack application using modern frameworks that served 500+ users, implementing CI/CD pipelines and automated testing."},
                {"question": "Where do you see yourself in 5 years?", "type": "situational", "tip": "Show ambition aligned with the role and company growth", "sample_answer": "I see myself growing into a senior role where I can mentor others while continuing to deepen my technical expertise and contribute to impactful projects."},
            ],
        }


@router.post("/career-compare")
def compare_careers(
    request: CareerCompareRequest,
    current_user: User = Depends(get_current_user),
):
    """Compare 2-3 career paths side by side"""
    from openai import OpenAI
    from config import get_settings
    import json, re

    settings = get_settings()

    user_skills_list = [skill.name for skill in current_user.skills]
    prompt = f"""Compare these careers for a student with skills in {', '.join(user_skills_list[:8])}:
Careers: {', '.join(request.careers[:3])}

Return ONLY a JSON array where each object represents one career:
[
  {{
    "title": "Career Title",
    "salary_range": "$XX,000 - $XX,000",
    "growth_outlook": "Strong/Moderate/Limited",
    "skill_match": 85,
    "work_life_balance": 7,
    "entry_barrier": "Low/Medium/High",
    "pros": ["pro1", "pro2", "pro3"],
    "cons": ["con1", "con2"],
    "time_to_entry": "X months/years"
  }}
]"""

    if not settings.openai_api_key:
        return {"careers": _build_career_compare_fallback(request.careers, user_skills_list)}

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career comparison analyst. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        content = response.choices[0].message.content
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        careers = json.loads(json_match.group()) if json_match else json.loads(content)
        return {"careers": careers}
    except Exception as e:
        print(f"Career compare AI error: {e}")
        return {"careers": _build_career_compare_fallback(request.careers, user_skills_list)}


def _build_career_compare_fallback(careers: List[str], user_skills: List[str]) -> List[Dict]:
    """Build differentiated fallback career comparison data"""
    career_data = {
        "frontend": {"salary_range": "$65,000 - $140,000", "growth_outlook": "Strong", "skill_match": 78, "work_life_balance": 8, "entry_barrier": "Low", "pros": ["High demand for web apps", "Creative and visual work", "Large open-source ecosystem"], "cons": ["Rapidly changing frameworks", "Browser compatibility issues"], "time_to_entry": "3-6 months"},
        "backend": {"salary_range": "$75,000 - $160,000", "growth_outlook": "Strong", "skill_match": 82, "work_life_balance": 7, "entry_barrier": "Medium", "pros": ["Higher average salary", "Scalable system design", "Strong job stability"], "cons": ["Less visual feedback", "Complex debugging"], "time_to_entry": "6-9 months"},
        "full stack": {"salary_range": "$70,000 - $155,000", "growth_outlook": "Strong", "skill_match": 80, "work_life_balance": 7, "entry_barrier": "Medium", "pros": ["Versatile skill set", "Can build complete products", "Highly employable"], "cons": ["Jack of all trades concern", "Harder to master both ends"], "time_to_entry": "6-12 months"},
        "data scientist": {"salary_range": "$85,000 - $170,000", "growth_outlook": "Strong", "skill_match": 72, "work_life_balance": 8, "entry_barrier": "High", "pros": ["Top-paying tech role", "Impactful insights", "Growing AI/ML demand"], "cons": ["Requires strong math background", "Data cleaning is tedious"], "time_to_entry": "9-18 months"},
        "devops": {"salary_range": "$80,000 - $165,000", "growth_outlook": "Strong", "skill_match": 68, "work_life_balance": 6, "entry_barrier": "High", "pros": ["Critical infrastructure role", "High demand", "Automation-focused"], "cons": ["On-call responsibilities", "Steep learning curve"], "time_to_entry": "6-12 months"},
        "product manager": {"salary_range": "$80,000 - $160,000", "growth_outlook": "Moderate", "skill_match": 65, "work_life_balance": 7, "entry_barrier": "Medium", "pros": ["Leadership opportunities", "Cross-functional impact", "No coding required"], "cons": ["Ambiguous success metrics", "High-pressure decisions"], "time_to_entry": "3-6 months"},
        "ux": {"salary_range": "$60,000 - $135,000", "growth_outlook": "Strong", "skill_match": 70, "work_life_balance": 8, "entry_barrier": "Low", "pros": ["Creative and empathetic work", "Growing demand", "User-centered impact"], "cons": ["Subjective feedback", "Requires strong portfolio"], "time_to_entry": "3-6 months"},
        "data analyst": {"salary_range": "$55,000 - $110,000", "growth_outlook": "Moderate", "skill_match": 75, "work_life_balance": 8, "entry_barrier": "Low", "pros": ["Great entry to data careers", "Business impact", "SQL-focused simplicity"], "cons": ["Can be repetitive", "Lower ceiling than data science"], "time_to_entry": "2-4 months"},
        "software engineer": {"salary_range": "$80,000 - $170,000", "growth_outlook": "Strong", "skill_match": 85, "work_life_balance": 7, "entry_barrier": "Medium", "pros": ["Excellent pay progression", "Remote-friendly", "Diverse specializations"], "cons": ["Continuous learning required", "Whiteboard interview culture"], "time_to_entry": "6-12 months"},
        "machine learning": {"salary_range": "$95,000 - $190,000", "growth_outlook": "Strong", "skill_match": 66, "work_life_balance": 7, "entry_barrier": "High", "pros": ["Cutting-edge technology", "Highest salary potential", "Research opportunities"], "cons": ["Heavy math prerequisites", "GPU costs for experimentation"], "time_to_entry": "12-24 months"},
    }
    
    result = []
    for i, career in enumerate(careers):
        career_lower = career.lower()
        matched = None
        for key, data in career_data.items():
            if key in career_lower or career_lower in key:
                matched = data
                break
        
        if not matched:
            # Generate unique fallback based on position
            base_salary = 60000 + i * 15000
            matched = {
                "salary_range": f"${base_salary:,} - ${base_salary + 60000:,}",
                "growth_outlook": ["Strong", "Moderate", "Strong"][i % 3],
                "skill_match": 70 + i * 7,
                "work_life_balance": 7 + (i % 2),
                "entry_barrier": ["Low", "Medium", "High"][i % 3],
                "pros": [f"Growing demand for {career}", "Good compensation", "Flexible work options"],
                "cons": ["Competitive market", "Requires continuous learning"],
                "time_to_entry": f"{3 + i * 3}-{6 + i * 3} months",
            }
        
        result.append({"title": career, **matched})
    return result


@router.get("/career-map")
def get_career_map(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get visual career map data — nodes and connections for career paths"""
    user_skills_list = [skill.name for skill in current_user.skills]
    profile = current_user.profile
    target_roles = profile.target_roles if profile and profile.target_roles else ["Software Engineer"]

    # Build a career map structure
    nodes = []
    edges = []

    # Current position node
    nodes.append({
        "id": "current",
        "label": "You Are Here",
        "type": "current",
        "skills": user_skills_list[:5],
    })

    # Target role nodes
    for i, role in enumerate(target_roles[:3]):
        role_id = f"target_{i}"
        nodes.append({
            "id": role_id,
            "label": role,
            "type": "target",
            "skills": [],
        })
        edges.append({"from": "current", "to": role_id, "label": "Learning Path"})

        # Related roles
        related = _get_related_roles(role)
        for j, rel in enumerate(related[:2]):
            rel_id = f"related_{i}_{j}"
            nodes.append({"id": rel_id, "label": rel, "type": "related", "skills": []})
            edges.append({"from": role_id, "to": rel_id, "label": "Growth Path"})

    return {"nodes": nodes, "edges": edges}


def _get_related_roles(role: str) -> List[str]:
    """Get related career titles"""
    role_map = {
        "Software Engineer": ["Senior Engineer", "Tech Lead", "Solutions Architect"],
        "Data Scientist": ["ML Engineer", "Data Engineering Lead", "AI Researcher"],
        "Product Manager": ["Senior PM", "Director of Product", "VP Product"],
        "UX Designer": ["Senior UX", "Design Lead", "Head of Design"],
        "DevOps Engineer": ["SRE", "Platform Engineer", "Cloud Architect"],
        "Full Stack Developer": ["Tech Lead", "Engineering Manager", "CTO"],
        "Frontend Developer": ["Senior Frontend", "UI Architect", "Design Engineer"],
        "Backend Developer": ["Senior Backend", "Systems Architect", "Principal Engineer"],
    }
    # Fuzzy match
    for key, related in role_map.items():
        if key.lower() in role.lower() or role.lower() in key.lower():
            return related
    return ["Senior " + role, role + " Lead", "Director of " + role.split()[-1]]
