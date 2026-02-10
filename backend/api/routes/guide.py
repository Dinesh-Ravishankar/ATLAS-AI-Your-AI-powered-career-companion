"""
Platform Guide API - Navigate Atlas AI with custom ML chatbot
Powered by RAG (Retrieval-Augmented Generation) + intent classification
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from config import get_db
from models.database import User
from auth.jwt_handler import get_current_user
from ai.platform_guide import platform_guide

router = APIRouter(prefix="/guide", tags=["Platform Guide"])


# ═══════════════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════

class GuideMessage(BaseModel):
    message: str
    history: List[Dict[str, str]] = []  # [{role: "user"/"assistant", content: "..."}]


class GuideResponse(BaseModel):
    response: str
    intent: str
    relevant_features: List[Dict]
    confidence: float
    action: Optional[Dict] = None  # {type: "navigate", route: "/dashboard/...", feature_name: "..."}
    timestamp: str


class FeatureInfo(BaseModel):
    id: str
    name: str
    route: str
    category: str
    description: str
    keywords: List[str]
    use_cases: List[str]


# ═══════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════

@router.get("/welcome")
def get_welcome_message():
    """Get initial welcome message for the platform guide"""
    return {
        "message": "👋 Hey! I'm your **Atlas AI Guide**. Think of me as your personal navigator for the platform.\n\n💡 Ask me anything like:\n- \"What can this platform do?\"\n- \"Help me find scholarships\"\n- \"I'm confused about my career\"\n- \"Show me how to build my portfolio\"\n\nWhat would you like to explore first?",
        "quick_actions": [
            {"label": "🗺️ Show me all features", "message": "What features does Atlas AI have?"},
            {"label": "🎯 Help me get started", "message": "I'm new here, guide me"},
            {"label": "💼 Career advice", "message": "I need career guidance"},
            {"label": "📚 Learning path", "message": "I want to learn new skills"}
        ]
    }


@router.post("/chat", response_model=GuideResponse)
def chat_with_guide(
    payload: GuideMessage,
    current_user: User = Depends(get_current_user)
):
    """
    Chat with the platform guide chatbot.
    Uses custom ML model with RAG + intent classification.
    """
    message = payload.message.strip()
    history = payload.history or []
    
    if not message:
        return GuideResponse(
            response="I didn't catch that. What would you like to know?",
            intent="empty",
            relevant_features=[],
            confidence=0.0,
            action=None,
            timestamp=datetime.utcnow().isoformat()
        )
    
    # Use custom ML model to generate response
    result = platform_guide.generate_response(message, history)
    
    return GuideResponse(
        response=result["response"],
        intent=result["intent"],
        relevant_features=result["relevant_features"],
        confidence=result["confidence"],
        action=result.get("action"),
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/features")
def get_all_features():
    """Get all platform features organized by category"""
    categorized = platform_guide.get_all_features_categorized()
    
    return {
        "categories": categorized,
        "total_features": len(platform_guide.knowledge_base)
    }


@router.get("/feature/{feature_id}")
def get_feature_detail(feature_id: str):
    """Get detailed information about a specific feature"""
    feature = next(
        (f for f in platform_guide.knowledge_base if f['id'] == feature_id),
        None
    )
    
    if not feature:
        return {"error": "Feature not found"}
    
    return feature


@router.post("/search")
def search_features(query: str):
    """Search for features using semantic search"""
    results = platform_guide.retrieve_relevant_features(query, top_k=5)
    
    return {
        "query": query,
        "results": [
            {
                "id": f["id"],
                "name": f["name"],
                "route": f["route"],
                "category": f["category"],
                "description": f["description"]
            }
            for f in results
        ],
        "count": len(results)
    }


@router.get("/health")
def guide_health_check():
    """Check if ML model is loaded and ready"""
    return {
        "status": "healthy",
        "ml_model": "loaded" if platform_guide.embedder else "fallback_mode",
        "llm": "available" if platform_guide.llm_client else "unavailable",
        "knowledge_base_size": len(platform_guide.knowledge_base),
        "embeddings_ready": platform_guide.feature_embeddings is not None
    }
