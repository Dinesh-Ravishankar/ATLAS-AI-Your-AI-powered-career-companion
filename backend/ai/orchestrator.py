"""
AI Orchestrator - LangChain-powered Career Counseling
Handles intelligent routing and conversation management
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config import get_settings
from typing import Dict, List, Optional
import json

settings = get_settings()


class CareerCounselorOrchestrator:
    """Main AI orchestrator for career guidance conversations"""
    
    def __init__(self):
        self.llm = None
        try:
            if settings.openai_api_key:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=settings.openai_api_key
                )
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI LLM: {e}")
            self.llm = None
        
    def create_career_counselor_chain(self, atlas_card: Dict):
        """Create a conversation chain with context from Atlas Card"""
        if not self.llm:
            return None
        
        # Build context from Atlas Card
        context = self._build_context(atlas_card)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are Atlas AI, a career guidance counselor helping students find clarity in their career journey.

User Context:
{context}

Your role:
- Provide personalized career advice based on the user's profile
- Suggest actionable next steps for skill development
- Help them explore career paths aligned with their interests
- Be encouraging, insightful, and conversational
- Keep responses concise (2-3 paragraphs max)

Remember: You're transforming confusion to clarity."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        return {"prompt": prompt, "llm": self.llm, "history": []}
    
    def _build_context(self, atlas_card: Dict) -> str:
        """Build context string from Atlas Card"""
        context_parts = []
        
        if atlas_card.get("full_name"):
            context_parts.append(f"Name: {atlas_card['full_name']}")
        
        if atlas_card.get("major"):
            context_parts.append(f"Major: {atlas_card['major']}")
        
        if atlas_card.get("university"):
            context_parts.append(f"University: {atlas_card['university']}")
        
        if atlas_card.get("graduation_year"):
            context_parts.append(f"Graduation Year: {atlas_card['graduation_year']}")
        
        if atlas_card.get("skills"):
            skills_list = ", ".join([s.get("name", s) if isinstance(s, dict) else s for s in atlas_card["skills"]])
            context_parts.append(f"Skills: {skills_list}")
        
        if atlas_card.get("target_roles"):
            target_roles_list = ", ".join(atlas_card["target_roles"])
            context_parts.append(f"Target Roles: {target_roles_list}")
        
        if atlas_card.get("interests"):
            interests_list = ", ".join(atlas_card["interests"])
            context_parts.append(f"Interests: {interests_list}")
        
        return "\n".join(context_parts) if context_parts else "No profile data available yet."
    
    def start_soft_skills_roleplay(self, scenario: str, atlas_card: Dict):
        """Initialize a soft skills role-play scenario"""
        context = self._build_context(atlas_card)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are Atlas AI, a soft skills coach. You are conducting a role-play simulation with a student.

Scenario: {scenario}

Student Profile:
{context}

Your objective:
- Adopt the character required for the scenario (e.g., manager, client, teammate)
- Push the student to demonstrate soft skills (communication, empathy, logic)
- After the user speaks 3-4 times, pause the role-play and provide a brief 'Coach's Feedback' on their performance.
- Be realistic and professional."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        if not self.llm:
            return None
        return {"prompt": prompt, "llm": self.llm, "history": []}

    def generate_career_roadmap(self, target_role: str, current_skills: List[str]):
        """Generate a detailed step-by-step career roadmap"""
        prompt = f"""Target Role: {target_role}
Current Skills: {', '.join(current_skills)}

Generate a 4-step actionable career roadmap. For each step provide:
1. Goal: What to achieve
2. Skills to learn: Key technical or soft skills
3. Resource Type: Recommendations (e.g., Projects, Certifications, Networking)
4. Estimated Timeline: Weeks/Months

Return as a JSON list of objects."""

        if not self.llm:
            return json.dumps(self._fallback_roadmap(target_role, current_skills))

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"OpenAI Error in generate_career_roadmap: {e}")
            return json.dumps(self._fallback_roadmap(target_role, current_skills))

    def _fallback_roadmap(self, target_role: str, current_skills: List[str]) -> List[Dict]:
        """Return a sensible fallback roadmap when AI is unavailable"""
        return [
            {"step": 1, "goal": f"Build foundation for {target_role}", "skills_to_learn": ["Core concepts", "Industry tools"], "resource_type": "Online courses & tutorials", "estimated_timeline": "4-6 weeks"},
            {"step": 2, "goal": "Develop practical projects", "skills_to_learn": ["Project management", "Version control"], "resource_type": "Personal projects & open source", "estimated_timeline": "6-8 weeks"},
            {"step": 3, "goal": "Build professional network", "skills_to_learn": ["Communication", "Industry knowledge"], "resource_type": "Networking events & LinkedIn", "estimated_timeline": "4-6 weeks"},
            {"step": 4, "goal": f"Apply for {target_role} positions", "skills_to_learn": ["Interview prep", "Resume optimization"], "resource_type": "Mock interviews & job boards", "estimated_timeline": "4-8 weeks"},
        ]

    def get_career_recommendations(self, atlas_card: Dict, preferences: Optional[Dict] = None) -> List[Dict]:
        """Generate AI-powered career recommendations"""
        
        context = self._build_context(atlas_card)
        pref_text = ""
        if preferences:
            pref_text = f"\nUser Preferences: {json.dumps(preferences)}"
        
        prompt = f"""Based on this student profile:
{context}{pref_text}

Suggest 5 career paths that would be a great fit. For each career, provide:
1. Job title
2. Match score (0-100)
3. Brief description (1 sentence)
4. 3 key required skills
5. Average salary range
6. Why it's a good match (2 reasons)

Format as JSON array."""

        if not self.llm:
            return self._fallback_recommendations(atlas_card)

        try:
            response = self.llm.invoke(prompt)
            # Parse AI response into structured format
            return self._parse_career_recommendations(response.content)
        except Exception as e:
            print(f"Error in get_career_recommendations: {e}")
            return self._fallback_recommendations(atlas_card)
    
    def _parse_career_recommendations(self, ai_response: str) -> List[Dict]:
        """Parse AI response into structured career recommendations"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback to structured mock data
        return [
            {
                "title": "Software Engineer",
                "match_score": 92,
                "description": "Build and maintain software applications and systems",
                "required_skills": ["Python", "JavaScript", "Problem Solving"],
                "average_salary": 95000,
                "growth_rate": 22,
                "reasons": [
                    "Strong technical background aligns well",
                    "High demand in current job market"
                ]
            },
            {
                "title": "Data Scientist",
                "match_score": 88,
                "description": "Analyze complex data to drive business decisions",
                "required_skills": ["Python", "Statistics", "Machine Learning"],
                "average_salary": 105000,
                "growth_rate": 35,
                "reasons": [
                    "Analytical skills match role requirements",
                    "Growing field with excellent opportunities"
                ]
            },
            {
                "title": "Product Manager",
                "match_score": 75,
                "description": "Guide product development from conception to launch",
                "required_skills": ["Communication", "Strategy", "User Research"],
                "average_salary": 110000,
                "growth_rate": 18,
                "reasons": [
                    "Leadership potential identified",
                    "Bridge between technical and business"
                ]
            }
        ]
    
    def _fallback_recommendations(self, atlas_card: Dict) -> List[Dict]:
        """Fallback recommendations if AI fails"""
        return self._parse_career_recommendations("")

    def get_scholarships(self, major: str, location: str = "") -> List[Dict]:
        """Find relevant scholarships based on major and location"""
        prompt = f"""As Atlas AI, find 5 diverse scholarship or financial aid opportunities for a student majoring in {major}.
        
        Location Context: {location}
        
        CATEGORIES TO INCLUDE (if applicable):
        1. Government Scholarships (National/State level)
        2. University-specific grants
        3. Private foundation awards
        4. Corporate-sponsored scholarships
        
        Return a JSON array of objects with:
        - name: Scholarship name
        - provider: Organization name
        - category: (e.g., "Government", "Private", "University", "Corporate")
        - amount: String (e.g., "$5,000", "Full Tuition")
        - deadline: Date or "Ongoing"
        - description: 2 sentences about eligibility and benefits
        - link: "https://example.com"
        """
        if not self.llm:
            return self._fallback_scholarships()

        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\[.*\]', response.content, re.DOTALL)
            return json.loads(json_match.group()) if json_match else []
        except Exception as e:
            print(f"OpenAI API Error in get_scholarships: {e}")
            return self._fallback_scholarships()

    def _fallback_scholarships(self) -> List[Dict]:
        """Return fallback scholarships when AI is unavailable"""
        return [
            {"name": "Federal Pell Grant", "provider": "U.S. Department of Education", "category": "Government", "amount": "Up to $7,395", "deadline": "June 30, 2026", "description": "Need-based federal grant for undergraduate students demonstrating financial need. No repayment required.", "link": "https://studentaid.gov/understand-aid/types/grants/pell"},
            {"name": "National SMART Grant", "provider": "Federal Government", "category": "Government", "amount": "Up to $4,000", "deadline": "Ongoing", "description": "For third and fourth year undergraduate students majoring in STEM fields with a GPA of 3.0 or higher.", "link": "https://studentaid.gov"},
            {"name": "Google Generation Scholarship", "provider": "Google", "category": "Corporate", "amount": "$10,000", "deadline": "December 2026", "description": "For students in computer science or related fields who demonstrate leadership and academic excellence.", "link": "https://buildyourfuture.withgoogle.com/scholarships"},
            {"name": "Adobe Research Women-in-Technology", "provider": "Adobe", "category": "Corporate", "amount": "$10,000", "deadline": "October 2026", "description": "Scholarship for female students pursuing degrees in technology, supporting diversity and innovation in the field.", "link": "https://research.adobe.com/scholarship"},
            {"name": "State Merit Scholarship", "provider": "State Department of Education", "category": "Government", "amount": "$2,500 - $5,000", "deadline": "March 31, 2026", "description": "Merit-based scholarship for in-state students with strong academic records and community involvement.", "link": "#"},
        ]

    def get_side_hustle_ideas(self, skills: List[str], interests: List[str]) -> List[Dict]:
        """Incubate side hustle ideas based on user's Skill DNA"""
        skills_str = ", ".join(skills)
        interests_str = ", ".join(interests)
        
        prompt = f"""As Atlas AI, brainstorm 5 profitable side hustle ideas for a student with these skills: {skills_str} and interests: {interests_str}.
        Focus on low-cost entry and high flexibility.
        
        Return a JSON array of objects with:
        - title: Name of the side hustle
        - potential_income: Monthly estimate (e.g., "$500-$1500")
        - time_commitment: Low/Medium/High
        - difficulty: Beginner/Intermediate/Advanced
        - description: 2 sentences on how to start
        - first_three_steps: Array of strings
        """
        if not self.llm:
            return self._fallback_side_hustles(skills)

        try:
            response = self.llm.invoke(prompt)
            import re
            json_match = re.search(r'\[.*\]', response.content, re.DOTALL)
            return json.loads(json_match.group()) if json_match else []
        except Exception as e:
            print(f"OpenAI API Error in get_side_hustle_ideas: {e}")
            return self._fallback_side_hustles(skills)

    def _fallback_side_hustles(self, skills: List[str]) -> List[Dict]:
        """Return fallback side hustles when AI is unavailable"""
        skills_lower = [s.lower() for s in skills]
        hustles = [
            {"title": "Freelance Web Development", "potential_income": "$500-$2000/mo", "time_commitment": "Medium", "difficulty": "Intermediate", "description": "Build websites and web apps for small businesses and startups. Use platforms like Upwork and Fiverr to find clients.", "first_three_steps": ["Create a portfolio website with 3 sample projects", "Set up profiles on Upwork and Fiverr", "Reach out to 10 local businesses"]},
            {"title": "Online Tutoring", "potential_income": "$300-$1500/mo", "time_commitment": "Low", "difficulty": "Beginner", "description": "Teach programming, math, or other subjects online. Flexible hours that fit around your class schedule.", "first_three_steps": ["Sign up on Wyzant or Chegg Tutors", "Create a compelling tutor profile", "Offer first session at a discount"]},
            {"title": "Content Creation & Blogging", "potential_income": "$200-$1000/mo", "time_commitment": "Medium", "difficulty": "Beginner", "description": "Start a tech blog or YouTube channel sharing tutorials and industry insights. Monetize through ads and sponsorships.", "first_three_steps": ["Choose a niche topic you know well", "Create 5 pieces of quality content", "Share on social media and dev communities"]},
            {"title": "UI/UX Design Freelancing", "potential_income": "$500-$2500/mo", "time_commitment": "Medium", "difficulty": "Intermediate", "description": "Design user interfaces and experiences for apps and websites. High demand with relatively low competition.", "first_three_steps": ["Build a Dribbble/Behance portfolio", "Take a UI/UX fundamentals course", "Start with small gigs on 99designs"]},
            {"title": "Tech Resume & LinkedIn Optimization", "potential_income": "$300-$800/mo", "time_commitment": "Low", "difficulty": "Beginner", "description": "Help job seekers optimize their resumes and LinkedIn profiles for tech roles. Leverage your industry knowledge.", "first_three_steps": ["Study ATS-friendly resume formats", "Offer free reviews to build testimonials", "Market on LinkedIn and Reddit"]},
        ]
        return hustles


# Global instance
orchestrator = CareerCounselorOrchestrator()


def chat_with_counselor(message: str, atlas_card: Dict, conversation_history: Optional[List] = None) -> str:
    """Main chat interface for career counseling with context and memory"""
    try:
        chain_data = orchestrator.create_career_counselor_chain(atlas_card)
        if not chain_data:
            return _fallback_counselor_response(message)
        
        # Build message history
        history = []
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    history.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    history.append(AIMessage(content=msg.get("content", "")))
        
        formatted = chain_data["prompt"].format_messages(history=history, input=message)
        response = chain_data["llm"].invoke(formatted)
        return response.content
    except Exception as e:
        print(f"Chat error: {e}")
        return _fallback_counselor_response(message)


def _fallback_counselor_response(message: str) -> str:
    """Provide a helpful response when AI is unavailable"""
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["resume", "cv"]):
        return "Great question about your resume! Here are key tips: 1) Tailor it to each job description, 2) Use action verbs and quantify achievements, 3) Keep it to 1 page as a student, 4) Include relevant projects and coursework. I'd also recommend using our Resume Builder feature for a polished result."
    if any(w in msg_lower for w in ["interview", "prepare"]):
        return "Interview preparation is crucial! Focus on: 1) Research the company thoroughly, 2) Practice the STAR method for behavioral questions, 3) Prepare 3-5 questions to ask the interviewer, 4) Do mock interviews with friends or use our Mock Interview feature. You've got this!"
    if any(w in msg_lower for w in ["skill", "learn", "course"]):
        return "Skill development is a great focus! I recommend: 1) Identify the top 3 skills in your target job descriptions, 2) Use free resources like freeCodeCamp, Coursera, and MIT OpenCourseWare, 3) Build projects to demonstrate skills, 4) Check out our Skill Gap Analyzer for a personalized learning plan."
    return "That's a great question! While my AI-powered response is currently limited, here are some general tips: 1) Focus on building a strong portfolio of projects, 2) Network through LinkedIn and local meetups, 3) Use your university's career services, 4) Explore our dashboard features like Skill Gap Analyzer, Career Compare, and Learning Path for personalized guidance. Feel free to ask me anything else!"


def get_ai_career_recommendations(atlas_card: Dict, preferences: Optional[Dict] = None) -> List[Dict]:
    """Get AI-powered career recommendations"""
    return orchestrator.get_career_recommendations(atlas_card, preferences)
