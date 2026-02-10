"""
Custom ML Platform Guide - RAG-based chatbot for navigating Atlas AI
Uses sentence embeddings + intent classification + GPT-4o-mini
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from datetime import datetime
import json
from config import get_settings

settings = get_settings()


# ═══════════════════════════════════════════════════════════
# KNOWLEDGE BASE — All Atlas AI features with embeddings
# ═══════════════════════════════════════════════════════════

ATLAS_KNOWLEDGE_BASE = [
    {
        "id": "career_coach",
        "name": "Career Clarity Coach",
        "route": "/dashboard/coach",
        "category": "AI Counseling",
        "description": "24/7 AI career counselor that helps you with career decisions, resume feedback, interview prep, and stress management. Provides personalized advice based on your profile.",
        "keywords": ["coach", "counselor", "advice", "career guidance", "help", "talk", "chat", "confused", "stuck"],
        "use_cases": ["Need career advice", "Feeling confused", "Want to talk", "Resume help", "Interview prep"],
        "example_questions": [
            "I'm confused about my career path",
            "Can someone help me?",
            "I need advice",
            "How do I improve my resume?"
        ]
    },
    {
        "id": "origin_story",
        "name": "The Origin Story",
        "route": "/dashboard/origin-story",
        "category": "Stream Selection",
        "description": "Interactive 5-minute quiz that helps high school students choose the right college stream/major. Uses Anti-Choice Filter, Ikigai matching, and Day-in-the-Life simulations.",
        "keywords": ["stream", "major", "college", "what to study", "engineering", "medicine", "confused", "12th grade", "after school"],
        "use_cases": ["Choosing a college major", "Don't know what to study", "Career path selection", "Confused about streams"],
        "example_questions": [
            "What should I study in college?",
            "Help me choose a major",
            "I don't know what stream to pick",
            "Should I do engineering or medicine?"
        ]
    },
    {
        "id": "career_quiz",
        "name": "Career Quiz",
        "route": "/dashboard/career-quiz",
        "category": "Assessment",
        "description": "Quick personality and interest assessment that recommends career paths aligned with your strengths, values, and interests.",
        "keywords": ["quiz", "assessment", "test", "personality", "interests", "strengths", "career match"],
        "use_cases": ["Discover career options", "Understand my strengths", "Career assessment"],
        "example_questions": [
            "What careers match my personality?",
            "Take a career assessment",
            "Find my dream job"
        ]
    },
    {
        "id": "skill_gap",
        "name": "Skill Gap Analysis",
        "route": "/dashboard/skill-gap",
        "category": "Skills",
        "description": "Analyzes the gap between your current skills and target role requirements. Shows missing skills, learning time, and priority levels.",
        "keywords": ["skills", "gap", "missing", "learn", "requirements", "what skills", "need to learn"],
        "use_cases": ["See missing skills", "Know what to learn", "Job requirements"],
        "example_questions": [
            "What skills do I need for this job?",
            "Am I ready for this role?",
            "What should I learn next?"
        ]
    },
    {
        "id": "learning_path",
        "name": "Learning Path",
        "route": "/dashboard/learning-path",
        "category": "Learning",
        "description": "Generates a personalized learning roadmap with courses, projects, and milestones to reach your target role. Includes timeline and weekly hour estimates.",
        "keywords": ["learning", "roadmap", "courses", "path", "how to learn", "study plan", "curriculum"],
        "use_cases": ["Get a learning plan", "Find courses", "Career roadmap"],
        "example_questions": [
            "How do I become a data scientist?",
            "Give me a learning roadmap",
            "What courses should I take?"
        ]
    },
    {
        "id": "career_map",
        "name": "Career Map",
        "route": "/dashboard/career-map",
        "category": "Exploration",
        "description": "Interactive visualization of career paths, showing progression from entry-level to senior roles with salary ranges and timelines.",
        "keywords": ["career path", "progression", "map", "growth", "senior level", "career ladder"],
        "use_cases": ["Visualize career progression", "See career paths", "Growth trajectory"],
        "example_questions": [
            "What's my career progression?",
            "Show me career paths",
            "How do I grow in my field?"
        ]
    },
    {
        "id": "career_compare",
        "name": "Career Compare",
        "route": "/dashboard/career-compare",
        "category": "Decision Making",
        "description": "Compare up to 3 careers side-by-side with salary, growth rate, work-life balance, required skills, and match percentage to your profile.",
        "keywords": ["compare", "vs", "difference", "which career", "better", "choose between"],
        "use_cases": ["Compare career options", "Choose between jobs", "Decision making"],
        "example_questions": [
            "Compare data scientist vs software engineer",
            "Which is better: X or Y?",
            "Help me choose between careers"
        ]
    },
    {
        "id": "projects",
        "name": "Project Ideas",
        "route": "/dashboard/projects",
        "category": "Portfolio",
        "description": "Get AI-generated project ideas tailored to your target role. Includes difficulty level, tech stack, and implementation timeline.",
        "keywords": ["projects", "portfolio", "build", "ideas", "practice", "hands-on"],
        "use_cases": ["Find project ideas", "Build portfolio", "Practice skills"],
        "example_questions": [
            "What projects should I build?",
            "Give me project ideas",
            "How to build my portfolio?"
        ]
    },
    {
        "id": "side_hustle",
        "name": "Side Hustle Finder",
        "route": "/dashboard/side-hustle",
        "category": "Income",
        "description": "Discover side income opportunities based on your skills. Shows hourly rates, time commitment, and getting started steps.",
        "keywords": ["side hustle", "money", "earn", "freelance", "gig", "extra income", "part-time"],
        "use_cases": ["Earn extra money", "Find freelance work", "Side income ideas"],
        "example_questions": [
            "How can I earn money on the side?",
            "Freelance opportunities for me",
            "Side income ideas"
        ]
    },
    {
        "id": "scholarships",
        "name": "Scholarship Finder",
        "route": "/dashboard/scholarships",
        "category": "Finance",
        "description": "Find scholarships, grants, and financial aid opportunities matched to your profile, field of study, and location.",
        "keywords": ["scholarship", "financial aid", "funding", "grants", "money for college", "free money"],
        "use_cases": ["Find scholarships", "Financial aid", "Reduce education costs"],
        "example_questions": [
            "Are there scholarships for me?",
            "How to pay for college?",
            "Find financial aid"
        ]
    },
    {
        "id": "job_verifier",
        "name": "Ghost Job Detector",
        "route": "/dashboard/verify-job",
        "category": "Job Search",
        "description": "Verify if a job posting is legitimate or a scam. Analyzes red flags, salary expectations, and company reputation.",
        "keywords": ["job scam", "fake job", "verify", "legitimate", "ghost job", "real or fake", "suspicious"],
        "use_cases": ["Verify job postings", "Avoid scams", "Check legitimacy"],
        "example_questions": [
            "Is this job posting real?",
            "How to avoid job scams?",
            "Check if this company is legit"
        ]
    },
    {
        "id": "github_import",
        "name": "GitHub Portfolio Import",
        "route": "/dashboard/github-import",
        "category": "Portfolio",
        "description": "Import your GitHub projects and automatically generate a professional portfolio showcasing your best work.",
        "keywords": ["github", "portfolio", "import", "projects", "showcase", "open source"],
        "use_cases": ["Import GitHub projects", "Auto-generate portfolio", "Showcase work"],
        "example_questions": [
            "Import my GitHub projects",
            "Create portfolio from GitHub",
            "Show my GitHub work"
        ]
    },
    {
        "id": "experience_translator",
        "name": "Experience Translator",
        "route": "/dashboard/experience-translator",
        "category": "Resume",
        "description": "Converts everyday experiences (club activities, volunteering, hobbies) into professional resume bullet points with impact metrics.",
        "keywords": ["resume", "experience", "translate", "bullet points", "no experience", "student activities"],
        "use_cases": ["Write better resume", "Convert activities to skills", "First resume help"],
        "example_questions": [
            "I have no work experience",
            "Turn my activities into resume points",
            "How to write my first resume?"
        ]
    },
    {
        "id": "trends",
        "name": "Career Trends",
        "route": "/dashboard/trends",
        "category": "Market Intelligence",
        "description": "Stay updated on emerging tech skills, industry trends, and job market insights. See what's hot and what's declining.",
        "keywords": ["trends", "hot skills", "emerging", "future", "in-demand", "market", "industry"],
        "use_cases": ["See market trends", "Future-proof skills", "What's in demand"],
        "example_questions": [
            "What skills are trending?",
            "What's hot in tech?",
            "Future job market trends"
        ]
    },
    {
        "id": "atlas_card",
        "name": "Atlas Card (Profile)",
        "route": "/dashboard/profile",
        "category": "Profile",
        "description": "Your digital career passport. Centralized profile with skills, experience, education, and career preferences.",
        "keywords": ["profile", "edit profile", "my details", "update info", "atlas card"],
        "use_cases": ["Update profile", "Edit details", "View my info"],
        "example_questions": [
            "Update my profile",
            "Edit my details",
            "Where's my profile?"
        ]
    },
    {
        "id": "privacy",
        "name": "Privacy Settings",
        "route": "/dashboard/privacy",
        "category": "Settings",
        "description": "Control your data privacy, manage what AI can access, and set visibility preferences.",
        "keywords": ["privacy", "data", "security", "settings", "control", "who can see"],
        "use_cases": ["Manage privacy", "Control data", "Security settings"],
        "example_questions": [
            "Privacy settings",
            "Control my data",
            "Who can see my info?"
        ]
    }
]


# ═══════════════════════════════════════════════════════════
# INTENT CLASSIFICATION — Custom ML classifier
# ═══════════════════════════════════════════════════════════

INTENT_PATTERNS = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "good morning", "good afternoon", "sup", "yo"],
        "response": "Hey! 👋 I'm your Atlas AI Guide. I help you navigate the platform and find the right features for you. What are you looking to do today?"
    },
    "lost": {
        "patterns": ["lost", "confused", "don't know", "help", "where", "how do i", "stuck"],
        "response": "No worries, I've got you! Let me help you find your way. What are you trying to do?"
    },
    "feature_list": {
        "patterns": ["what can you do", "features", "show me", "list", "all features", "capabilities"],
        "response": "Atlas AI has 15+ powerful features! Here are the categories:\n\n🤖 **AI Counseling:** Career Coach\n📚 **Learning:** Skill Gap, Learning Path\n💼 **Career Planning:** Quiz, Compare, Map, Origin Story\n💰 **Opportunities:** Side Hustles, Scholarships, Job Verifier\n🚀 **Portfolio:** Projects, GitHub Import, Experience Translator\n📊 **Intelligence:** Trends, Privacy\n\nWhat interests you most?"
    },
    "how_to_navigate": {
        "patterns": ["how to use", "navigate", "tutorial", "guide", "getting started", "new here"],
        "response": "Welcome to Atlas AI! Here's how to get started:\n\n1️⃣ **Update your Atlas Card** (Profile) with your skills & goals\n2️⃣ **Take the Career Quiz** to discover your strengths\n3️⃣ **Talk to the Career Coach** for personalized advice\n4️⃣ **Explore features** from the sidebar based on your needs\n\nWhat would you like to start with?"
    },
    "thank_you": {
        "patterns": ["thank", "thanks", "appreciate", "helpful"],
        "response": "You're welcome! 😊 I'm here whenever you need me. Feel free to ask anything about the platform!"
    }
}


# ═══════════════════════════════════════════════════════════
# RAG - RETRIEVAL AUGMENTED GENERATION ENGINE
# ═══════════════════════════════════════════════════════════

class PlatformGuideML:
    """Custom ML model for platform navigation using RAG + intent classification"""
    
    def __init__(self):
        self.knowledge_base = ATLAS_KNOWLEDGE_BASE
        self.embedder = None
        self.feature_embeddings = None
        self.llm_client = None
        
        # Initialize embedder
        # self._init_embedder()
        
        # Initialize OpenAI client if available
        # self._init_llm()
    
    def ensure_initialized(self):
        """Lazy load models if not already loaded"""
        if not self.embedder and not hasattr(self, '_embedder_failed'):
            print("🚀 Loading Platform Guide ML models...")
            self._init_embedder()
            self._init_llm()
            if not self.embedder:
                self._embedder_failed = True
    
    def _init_embedder(self):
        """Initialize sentence transformer for semantic search"""
        try:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Pre-compute embeddings for all features
            self.feature_embeddings = {}
            for feature in self.knowledge_base:
                # Combine all searchable text
                text = f"{feature['name']} {feature['description']} {' '.join(feature['keywords'])} {' '.join(feature['use_cases'])}"
                embedding = self.embedder.encode(text)
                self.feature_embeddings[feature['id']] = embedding
            
            print("✅ Platform Guide ML: Embeddings initialized")
        except Exception as e:
            print(f"⚠️  Platform Guide ML: Could not load embeddings: {e}")
            self.embedder = None
    
    def _init_llm(self):
        """Initialize OpenAI client for conversational responses"""
        try:
            if settings.openai_api_key:
                from openai import OpenAI
                self.llm_client = OpenAI(api_key=settings.openai_api_key)
                print("✅ Platform Guide ML: LLM initialized")
        except Exception as e:
            print(f"⚠️  Platform Guide ML: LLM not available: {e}")
            self.llm_client = None
    
    def classify_intent(self, message: str) -> Optional[str]:
        """Classify user intent using pattern matching"""
        message_lower = message.lower().strip()
        
        for intent, data in INTENT_PATTERNS.items():
            for pattern in data["patterns"]:
                if pattern in message_lower:
                    return intent
        return None
    
    def retrieve_relevant_features(self, query: str, top_k: int = 3) -> List[Dict]:
        """RAG: Retrieve most relevant features using semantic search"""
        self.ensure_initialized()
        
        if not self.embedder or not self.feature_embeddings:
            # Fallback to keyword matching
            return self._keyword_search(query, top_k)
        
        # Encode query
        query_embedding = self.embedder.encode(query)
        
        # Calculate cosine similarity with all features
        similarities = []
        for feature_id, feature_embedding in self.feature_embeddings.items():
            similarity = np.dot(query_embedding, feature_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(feature_embedding)
            )
            feature = next(f for f in self.knowledge_base if f['id'] == feature_id)
            similarities.append((similarity, feature))
        
        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [feature for _, feature in similarities[:top_k]]
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """Fallback keyword-based search"""
        query_lower = query.lower()
        matches = []
        
        for feature in self.knowledge_base:
            score = 0
            # Check keywords
            for keyword in feature['keywords']:
                if keyword in query_lower:
                    score += 2
            # Check name
            if feature['name'].lower() in query_lower:
                score += 5
            # Check description
            for word in query_lower.split():
                if word in feature['description'].lower():
                    score += 1
            
            if score > 0:
                matches.append((score, feature))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        return [feature for _, feature in matches[:top_k]]
    
    def generate_response(self, message: str, conversation_history: List[Dict] = None) -> Dict:
        """Main method: Generate intelligent response using ML pipeline"""
        self.ensure_initialized()
        
        # Step 1: Check for direct intent patterns
        intent = self.classify_intent(message)
        if intent and intent in INTENT_PATTERNS:
            return {
                "response": INTENT_PATTERNS[intent]["response"],
                "intent": intent,
                "relevant_features": [],
                "confidence": 1.0,
                "action": None
            }
        
        # Step 2: Retrieve relevant features using RAG
        relevant_features = self.retrieve_relevant_features(message, top_k=3)
        
        # Step 3: Generate response using LLM if available
        if self.llm_client and relevant_features:
            response_text = self._generate_llm_response(message, relevant_features, conversation_history)
        else:
            # Fallback to template-based response
            response_text = self._generate_template_response(message, relevant_features)
        
        # Determine action (redirect to feature)
        action = None
        if relevant_features and len(relevant_features) == 1:
            # High confidence single match
            action = {
                "type": "navigate",
                "route": relevant_features[0]["route"],
                "feature_name": relevant_features[0]["name"]
            }
        
        return {
            "response": response_text,
            "intent": "feature_query",
            "relevant_features": [
                {
                    "id": f["id"],
                    "name": f["name"],
                    "route": f["route"],
                    "description": f["description"]
                }
                for f in relevant_features
            ],
            "confidence": 0.8 if relevant_features else 0.3,
            "action": action
        }
    
    def _generate_llm_response(self, message: str, features: List[Dict], history: List[Dict]) -> str:
        """Use GPT-4o-mini to generate natural response"""
        try:
            # Build context from relevant features
            features_context = "\n\n".join([
                f"**{f['name']}** ({f['route']})\n{f['description']}"
                for f in features
            ])
            
            # Build conversation history
            messages = [
                {
                    "role": "system",
                    "content": f"""You are the Atlas AI Platform Guide. Your job is to help users navigate the platform and find the right features.

Available features context:
{features_context}

Guidelines:
- Be friendly, concise, and helpful
- Recommend the most relevant feature based on the user's question
- Provide clear next steps
- Keep responses under 100 words
- Use emojis sparingly for friendliness"""
                }
            ]
            
            # Add history if provided
            if history:
                for msg in history[-4:]:  # Last 4 messages
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            messages.append({"role": "user", "content": message})
            
            response = self.llm_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._generate_template_response(message, features)
    
    def _generate_template_response(self, message: str, features: List[Dict]) -> str:
        """Fallback template-based response"""
        if not features:
            return "I'm not quite sure what you're looking for. Could you rephrase that? Or ask me 'What can you do?' to see all features."
        
        if len(features) == 1:
            f = features[0]
            return f"Based on your question, I think **{f['name']}** is what you need! 🎯\n\n{f['description']}\n\nClick below to go there, or I can help you with something else!"
        
        # Multiple matches
        response = "I found a few features that might help:\n\n"
        for i, f in enumerate(features, 1):
            response += f"{i}. **{f['name']}** — {f['description'][:80]}...\n"
        response += "\nWhich one interests you?"
        return response
    
    def get_all_features_categorized(self) -> Dict[str, List[Dict]]:
        """Get all features organized by category"""
        categorized = {}
        for feature in self.knowledge_base:
            category = feature['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append({
                "id": feature["id"],
                "name": feature["name"],
                "route": feature["route"],
                "description": feature["description"]
            })
        return categorized


# Global instance
platform_guide = PlatformGuideML()
