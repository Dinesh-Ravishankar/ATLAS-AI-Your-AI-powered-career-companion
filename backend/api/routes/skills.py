"""
Skills Routes
ESCO-powered skill search, soft-skills bootcamp, GitHub import
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from config import get_db
from models.database import User, Profile, Skill, user_skills
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])


class SkillSearchRequest(BaseModel):
    query: str
    limit: int = 10


class GitHubImportRequest(BaseModel):
    username: str


class ExperienceTranslateRequest(BaseModel):
    experience_type: str  # e.g. "retail", "babysitting", "volunteer"
    description: str
    duration: Optional[str] = None


class SoftSkillAssessment(BaseModel):
    answers: Dict[str, int]  # question_id -> 1-5 rating


# ESCO skill search
@router.post("/search")
def search_skills(request: SkillSearchRequest):
    """Search for skills using ESCO API"""
    try:
        from ai.esco_client import search_skills as esco_search
        results = esco_search(request.query, limit=request.limit)
        return {"skills": results}
    except Exception as e:
        # Fallback mock results
        return {
            "skills": [
                {"name": request.query.title(), "uri": None, "category": "technical"},
            ]
        }


@router.get("/esco/{role}")
def get_role_skills(role: str):
    """Get required skills for a role from ESCO"""
    try:
        from ai.esco_client import get_skills_for_role
        skills = get_skills_for_role(role)
        return {"role": role, "skills": skills}
    except Exception as e:
        return {"role": role, "skills": [], "error": str(e)}


# GitHub skills import
@router.post("/github-import")
async def import_github_skills_route(
    request: GitHubImportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Import skills from GitHub profile"""
    from ai.github_integration import import_github_skills

    result = await import_github_skills(request.username)
    if not result:
        raise HTTPException(status_code=404, detail=f"GitHub user '{request.username}' not found or API error")

    # Auto-add extracted skills to user profile
    added_skills = []
    for skill_name in result.get("skills", [])[:20]:
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
                    proficiency=0.6,
                    source="github",
                )
            )
            added_skills.append(skill_name)

    # Award XP
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + 200

    db.commit()

    return {
        "github_profile": result.get("profile"),
        "extracted_skills": result.get("skills"),
        "top_languages": result.get("top_languages"),
        "projects": result.get("projects"),
        "skills_added": added_skills,
        "xp_earned": 200,
    }


# Experience translator
@router.post("/translate-experience")
def translate_experience_route(
    request: ExperienceTranslateRequest,
    current_user: User = Depends(get_current_user),
):
    """Translate non-traditional experience into professional skills"""
    from ai.experience_translator import translate_experience

    result = translate_experience(
        experience_type=request.experience_type,
        description=request.description,
        duration=request.duration,
    )

    return result


# Soft skills bootcamp
SOFT_SKILL_MODULES = [
    {
        "id": "communication",
        "name": "Communication",
        "icon": "💬",
        "description": "Master written and verbal communication for professional settings",
        "lessons": [
            {"id": "comm_1", "title": "Active Listening", "duration": "15 min"},
            {"id": "comm_2", "title": "Email Etiquette", "duration": "10 min"},
            {"id": "comm_3", "title": "Presenting Ideas", "duration": "20 min"},
        ],
    },
    {
        "id": "teamwork",
        "name": "Teamwork",
        "icon": "🤝",
        "description": "Learn to collaborate effectively in diverse teams",
        "lessons": [
            {"id": "team_1", "title": "Conflict Resolution", "duration": "15 min"},
            {"id": "team_2", "title": "Giving Feedback", "duration": "10 min"},
            {"id": "team_3", "title": "Remote Collaboration", "duration": "15 min"},
        ],
    },
    {
        "id": "leadership",
        "name": "Leadership",
        "icon": "🏆",
        "description": "Develop leadership skills for any career stage",
        "lessons": [
            {"id": "lead_1", "title": "Decision Making", "duration": "15 min"},
            {"id": "lead_2", "title": "Delegation", "duration": "10 min"},
            {"id": "lead_3", "title": "Motivating Others", "duration": "15 min"},
        ],
    },
    {
        "id": "time_management",
        "name": "Time Management",
        "icon": "⏰",
        "description": "Optimize your productivity and meet deadlines",
        "lessons": [
            {"id": "time_1", "title": "Prioritization Frameworks", "duration": "15 min"},
            {"id": "time_2", "title": "Pomodoro Technique", "duration": "10 min"},
            {"id": "time_3", "title": "Avoiding Burnout", "duration": "15 min"},
        ],
    },
    {
        "id": "problem_solving",
        "name": "Problem Solving",
        "icon": "🧩",
        "description": "Approach problems systematically and creatively",
        "lessons": [
            {"id": "prob_1", "title": "Root Cause Analysis", "duration": "15 min"},
            {"id": "prob_2", "title": "Design Thinking", "duration": "20 min"},
            {"id": "prob_3", "title": "Critical Thinking", "duration": "15 min"},
        ],
    },
]


@router.get("/soft-skills/modules")
def get_soft_skill_modules():
    """Get all soft skills bootcamp modules"""
    return {"modules": SOFT_SKILL_MODULES}


@router.get("/soft-skills/module/{module_id}")
def get_soft_skill_module(module_id: str):
    """Get a specific soft skill module with lessons"""
    module = next((m for m in SOFT_SKILL_MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.post("/soft-skills/assess")
def assess_soft_skills(
    assessment: SoftSkillAssessment,
    current_user: User = Depends(get_current_user),
):
    """Assess user's soft skills based on self-evaluation"""
    scores = assessment.answers
    categories = {
        "communication": ["comm_1", "comm_2", "comm_3"],
        "teamwork": ["team_1", "team_2", "team_3"],
        "leadership": ["lead_1", "lead_2", "lead_3"],
        "time_management": ["time_1", "time_2", "time_3"],
        "problem_solving": ["prob_1", "prob_2", "prob_3"],
    }

    results = []
    for category, question_ids in categories.items():
        cat_scores = [scores.get(qid, 3) for qid in question_ids]
        avg = sum(cat_scores) / max(len(cat_scores), 1)
        results.append({
            "skill": category.replace("_", " ").title(),
            "score": round(avg, 1),
            "max_score": 5,
            "level": "strong" if avg >= 4 else ("developing" if avg >= 3 else "needs work"),
        })

    return {"assessment": results, "overall": round(sum(r["score"] for r in results) / len(results), 1)}


# Gamification stats
@router.get("/gamification")
def get_gamification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get gamification stats for current user"""
    from utils.gamification import get_gamification_summary

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        return get_gamification_summary(0, {})

    total_xp = profile.xp or 0
    # Build actions from profile state
    user_actions = {
        "complete_profile": bool(profile.bio and profile.major),
        "take_career_quiz": bool(profile.target_roles and len(profile.target_roles) > 0),
        "github_import": bool(profile.github_url),
        "projects_3": len(current_user.projects) >= 3,
    }

    return get_gamification_summary(total_xp, user_actions)


# General Assessments (Technical, Domain, Soft)
@router.get("/assessments")
def get_all_assessments():
    """Get all available assessments"""
    return [
        {
            "id": 1,
            "title": "Frontend Mastery",
            "category": "technical",
            "skill": "React & Frontend",
            "difficulty": "Intermediate",
            "questions_count": 5,
            "duration_minutes": 15,
            "completed": False,  # In real app, check DB
            "score": 0
        },
        {
            "id": 2,
            "title": "Backend Fundamentals",
            "category": "technical",
            "skill": "Python & API Design",
            "difficulty": "Intermediate",
            "questions_count": 5,
            "duration_minutes": 20,
            "completed": False,
            "score": 0
        },
        {
            "id": 3,
            "title": "Leadership Styles",
            "category": "soft",
            "skill": "Leadership",
            "difficulty": "Beginner",
            "questions_count": 3,
            "duration_minutes": 10,
            "completed": False,
            "score": 0
        },
         {
            "id": 4,
            "title": "Product Management 101",
            "category": "domain",
            "skill": "Product Management",
            "difficulty": "Beginner",
            "questions_count": 5,
            "duration_minutes": 15,
            "completed": False,
            "score": 0
        }
    ]


@router.get("/assessments/{assessment_id}")
def get_assessment_questions(assessment_id: int):
    """Get questions for a specific assessment"""
    # Mock data - in real app would come from DB
    if assessment_id == 1:  # Frontend
        return {
            "id": 1,
            "title": "Frontend Mastery",
            "questions": [
                {
                    "id": 1,
                    "text": "Which hook is used to perform side effects in React?",
                    "options": ["useState", "useEffect", "useContext", "useReducer"],
                    "correct_index": 1
                },
                {
                    "id": 2,
                    "text": "What does CSS Box Model consist of?",
                    "options": ["Margin, Border, Padding, Content", "Border, Background, Text, Image", "Padding, Float, Display, Width", "Content, Table, Flex, Grid"],
                    "correct_index": 0
                },
                 {
                    "id": 3,
                    "text": "Which method is used to update state based on previous state?",
                    "options": ["setState(newValue)", "setState(prev => newValue)", "updateState(val)", "state = val"],
                    "correct_index": 1
                },
                {
                    "id": 4,
                    "text": "What is the virtual DOM?",
                    "options": ["A direct copy of the browser DOM", "A lightweight copy of the DOM kept in memory", "A database for HTML elements", "A browser extension"],
                    "correct_index": 1
                },
                {
                    "id": 5,
                    "text": "In TypeScript, what type represents ‘any value’?",
                    "options": ["void", "never", "any", "unknown"],
                    "correct_index": 2
                }
            ]
        }
    elif assessment_id == 2: # Backend
         return {
            "id": 2,
            "title": "Backend Fundamentals",
            "questions": [
                {"id": 1, "text": "What does REST stand for?", "options": ["Representational State Transfer", "Remote Execution State Transfer", "Real State Transmission", "Reliable Server Transfer"], "correct_index": 0},
                {"id": 2, "text": "Which HTTP method is idempotent?", "options": ["POST", "PUT", "PATCH", "CONNECT"], "correct_index": 1},
                {"id": 3, "text": "What is a primary key?", "options": ["A key to encrypt data", "A unique identifier for a record", "The first column in a table", "A foreign key to another table"], "correct_index": 1},
                {"id": 4, "text": "What is dependency injection?", "options": ["Installing libraries", "Passing dependencies to a client", "Injecting code into a running process", "A security vulnerability"], "correct_index": 1},
                {"id": 5, "text": "Status code for 'Not Found'?", "options": ["200", "500", "403", "404"], "correct_index": 3}
            ]
        }
    
    # Default fallback
    return {
        "id": assessment_id,
        "title": "General Assessment",
        "questions": [
            {"id": 1, "text": "Sample Question 1?", "options": ["A", "B", "C", "D"], "correct_index": 0},
            {"id": 2, "text": "Sample Question 2?", "options": ["A", "B", "C", "D"], "correct_index": 1}
        ]
    }


class AssessmentSubmission(BaseModel):
    answers: Dict[str, int]  # question_id -> selected_index


@router.post("/assessments/{assessment_id}/submit")
def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit assessment and calculate score"""
    # Simple scoring logic
    questions = get_assessment_questions(assessment_id)["questions"]
    score = 0
    total = len(questions)
    
    for q in questions:
        q_id = str(q["id"])
        if q_id in submission.answers and submission.answers[q_id] == q["correct_index"]:
            score += 1
            
    percentage = int((score / total) * 100)
    
    # Award XP
    xp_gained = 50 + (score * 10)
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.xp = (profile.xp or 0) + xp_gained
        db.commit()
        
    return {
        "score": percentage,
        "correct_count": score,
        "total_questions": total,
        "xp_earned": xp_gained,
        "passed": percentage >= 70,
        "recommendations": ["Review the documentation for missed topics", "Practice with a mini-project"] if percentage < 100 else ["Great job! Move to advanced topics."]
    }
