"""
Career Clarity Coach — 24/7 AI Career Counselor
Persistent chat interface with deep context awareness.
Falls back gracefully when OpenAI quota is exhausted.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from config import get_db, get_settings
from models.database import User
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/coach", tags=["Career Clarity Coach"])

settings = get_settings()

# ── Request / Response models ──────────────────────────────

class CoachMessage(BaseModel):
    message: str
    history: Optional[List[Dict]] = []
    context: Optional[str] = "general"  # general | resume | interview | career | skills


class CoachResponse(BaseModel):
    response: str
    suggestions: List[str]
    timestamp: str
    context: str


# ── Fallback topic-aware responses ─────────────────────────

COACH_RESPONSES: Dict[str, Dict] = {
    "career": {
        "keywords": ["career", "job", "profession", "role", "path", "switch", "transition", "field"],
        "response": (
            "Great question about your career path! Let me share some structured advice:\n\n"
            "**1. Self-Assessment First**\n"
            "Before choosing a path, audit your skills, interests, and values. Our Skill Gap Analyzer can help map where you stand.\n\n"
            "**2. Explore, Don't Commit Blindly**\n"
            "Try informational interviews — reach out to 3-5 professionals on LinkedIn in roles you're curious about. Most people love sharing their journey.\n\n"
            "**3. Market Alignment**\n"
            "Check our Trends page to see which fields are growing. Align your passion with market demand for the best outcomes.\n\n"
            "**4. Start Small**\n"
            "Take a free course, do a weekend project, or shadow someone before making a big switch. The Career Compare tool can help you weigh options side-by-side."
        ),
        "suggestions": ["Analyze my skill gaps", "Compare two careers", "Show trending skills", "Generate a learning path"],
    },
    "resume": {
        "keywords": ["resume", "cv", "cover letter", "application", "apply"],
        "response": (
            "Let's get your resume in shape! Here's a proven framework:\n\n"
            "**The STAR-Plus Resume Method:**\n"
            "• **S**ummary — 2-line personal pitch tailored to the role\n"
            "• **T**echnical Skills — Match keywords from the job description\n"
            "• **A**chievements — Quantify everything (\"Increased sales by 30%\", not \"helped with sales\")\n"
            "• **R**elevant Projects — Show, don't tell. Link to GitHub/portfolio\n"
            "• **+** Education & Certifications\n\n"
            "**Pro Tips:**\n"
            "1. One page for < 5 years experience\n"
            "2. Use action verbs: Built, Led, Designed, Optimized\n"
            "3. Tailor for EACH application — ATS systems filter generic resumes\n"
            "4. Export a polished resume from your Atlas Card using our Resume Builder!"
        ),
        "suggestions": ["Export my resume", "Review my Atlas Card", "What skills should I add?", "Help with cover letter"],
    },
    "interview": {
        "keywords": ["interview", "prepare", "question", "behavioral", "technical", "negotiate", "salary"],
        "response": (
            "Interview prep is where most candidates win or lose. Here's your battle plan:\n\n"
            "**Before the Interview:**\n"
            "• Research the company's recent news, culture, and tech stack\n"
            "• Prepare 5 stories using the STAR method (Situation, Task, Action, Result)\n"
            "• Have 3 smart questions ready (about team, growth, challenges)\n\n"
            "**During the Interview:**\n"
            "• Listen fully before answering — pause 2 seconds to think\n"
            "• For technical: think out loud, explain your reasoning\n"
            "• For behavioral: be specific, use real examples with numbers\n\n"
            "**After the Interview:**\n"
            "• Send a thank-you email within 24 hours\n"
            "• Reference something specific from the conversation\n\n"
            "**Salary Negotiation:**\n"
            "Never give a number first. Say: \"I'd love to learn about the full compensation package for this role.\""
        ),
        "suggestions": ["Practice mock interview", "Common behavioral questions", "How to negotiate salary", "What to wear"],
    },
    "skills": {
        "keywords": ["skill", "learn", "course", "certificate", "improve", "upskill", "bootcamp", "tutorial"],
        "response": (
            "Smart focus on skill-building! Here's a strategic approach:\n\n"
            "**The 70-20-10 Learning Rule:**\n"
            "• **70%** — Hands-on projects (build real things)\n"
            "• **20%** — Learning from others (mentors, code reviews, pair programming)\n"
            "• **10%** — Formal courses (Coursera, Udemy, books)\n\n"
            "**Skill Prioritization Framework:**\n"
            "1. List the top 5 skills from your target job descriptions\n"
            "2. Score yourself 1-10 on each\n"
            "3. Focus on the biggest gap that appears most frequently\n\n"
            "**Free Resources:**\n"
            "• FreeCodeCamp, The Odin Project, CS50 (Harvard)\n"
            "• YouTube channels: Fireship, Traversy Media, 3Blue1Brown\n"
            "• Practice: LeetCode, HackerRank, Kaggle\n\n"
            "Use our Learning Path generator for a personalized roadmap!"
        ),
        "suggestions": ["Generate my learning path", "Analyze my skill gaps", "Find scholarships", "Recommend projects"],
    },
    "stress": {
        "keywords": ["stress", "anxious", "overwhelm", "confused", "lost", "scared", "worried", "burnout", "tired", "depressed", "help"],
        "response": (
            "I hear you, and it's completely normal to feel this way. Career decisions are big, and uncertainty is part of the process. Let me help you reframe:\n\n"
            "**1. You're Not Behind**\n"
            "There is no \"right\" timeline. People switch careers at 25, 35, and 55. Your journey is yours.\n\n"
            "**2. Small Steps > Big Leaps**\n"
            "You don't need to figure it all out today. Pick ONE small action: update your profile, take a free course, or explore one new career path.\n\n"
            "**3. The 5-5-5 Rule**\n"
            "Ask yourself: Will this matter in 5 days? 5 months? 5 years? Most worries fade faster than we think.\n\n"
            "**4. Talk to Someone**\n"
            "If stress is persistent, your university counseling center is free and confidential. There's zero shame in using it.\n\n"
            "I'm here 24/7 — you can always come back and we'll figure this out together, one step at a time. 💙"
        ),
        "suggestions": ["Show me easy wins", "What careers match my skills?", "Help me make a plan", "I need motivation"],
    },
    "general": {
        "keywords": [],
        "response": (
            "I'm Atlas AI, your personal career clarity coach! I'm here 24/7 to help you navigate your career journey. Here's what I can help with:\n\n"
            "🎯 **Career Exploration** — Discover paths that match your skills and interests\n"
            "📊 **Skill Analysis** — Identify gaps and build a learning plan\n"
            "📝 **Resume & Applications** — Craft compelling applications\n"
            "🎤 **Interview Prep** — Practice and get tips\n"
            "💰 **Financial Planning** — Find scholarships and side hustles\n"
            "🧭 **Decision Support** — Compare options with data\n\n"
            "Just ask me anything — I'm like having a career counselor in your pocket, minus the 376:1 ratio. 😄\n\n"
            "What would you like to explore?"
        ),
        "suggestions": ["What career fits me?", "Help with my resume", "Prepare for an interview", "I feel stuck"],
    },
}


def _detect_context(message: str) -> str:
    """Detect the conversation context from the message."""
    msg_lower = message.lower()
    for ctx, data in COACH_RESPONSES.items():
        if ctx == "general":
            continue
        if any(kw in msg_lower for kw in data["keywords"]):
            return ctx
    return "general"


def _get_coach_response(message: str, user_context: Dict) -> Dict:
    """Generate a coach response — tries LLM first, falls back to curated responses."""
    context = _detect_context(message)

    # Try LLM if available
    try:
        if settings.openai_api_key:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)

            system_prompt = f"""You are Atlas AI, a warm, knowledgeable 24/7 career clarity coach.
User Profile: {user_context}

Your style:
- Empathetic but actionable — always end with concrete next steps
- Use markdown formatting (bold, bullet points)
- Keep responses 150-250 words
- Reference Atlas AI features when relevant (Skill Gap, Career Compare, Learning Path, etc.)
- If the student seems stressed, be supportive first, practical second
- Never be preachy or generic — give specific, personalized advice"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            ai_text = response.choices[0].message.content
            fallback = COACH_RESPONSES.get(context, COACH_RESPONSES["general"])
            return {
                "response": ai_text,
                "suggestions": fallback["suggestions"],
                "context": context,
            }
    except Exception as e:
        print(f"Coach LLM error: {e}")

    # Fallback to curated responses
    fallback = COACH_RESPONSES.get(context, COACH_RESPONSES["general"])
    return {
        "response": fallback["response"],
        "suggestions": fallback["suggestions"],
        "context": context,
    }


# ── Endpoints ─────────────────────────────────────────────

@router.post("/chat", response_model=CoachResponse)
def coach_chat(
    msg: CoachMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Chat with the Career Clarity Coach."""
    # Build user context for personalization
    user_context = {
        "name": current_user.full_name,
        "skills": [s.name for s in current_user.skills][:10],
    }
    if current_user.profile:
        p = current_user.profile
        user_context.update({
            "major": p.major,
            "university": p.university,
            "interests": p.interests or [],
            "target_roles": p.target_roles or [],
        })

    result = _get_coach_response(msg.message, user_context)

    return CoachResponse(
        response=result["response"],
        suggestions=result["suggestions"],
        timestamp=datetime.now().isoformat(),
        context=result["context"],
    )


@router.get("/welcome")
def coach_welcome(current_user: User = Depends(get_current_user)):
    """Get a personalized welcome message."""
    name = current_user.full_name or "there"
    first = name.split()[0]
    skills_count = len(current_user.skills)
    has_profile = current_user.profile is not None

    if not has_profile or skills_count == 0:
        return {
            "message": f"Hey {first}! 👋 Welcome to your personal career coach. I notice you haven't set up your Atlas Card yet — let's fix that first so I can give you personalized advice!",
            "suggestions": ["Set up my profile", "What can you help with?", "I'm feeling overwhelmed", "Explore careers"],
        }

    return {
        "message": f"Welcome back, {first}! 👋 You've got {skills_count} skills on your profile. What would you like to work on today?",
        "suggestions": ["Analyze my skill gaps", "Help with my resume", "Compare career paths", "I need a learning plan"],
    }
