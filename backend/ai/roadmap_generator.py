"""
AI-powered Learning Roadmap Generator
Generates personalized learning paths with milestones, resources, and timelines
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import get_settings

_settings = get_settings()

# Initialize OpenAI client
client = OpenAI(api_key=_settings.openai_api_key) if _settings.openai_api_key else None

# Skill difficulty mapping (learning time in weeks)
SKILL_LEARNING_TIME = {
    "beginner": {
        "programming": 12,
        "data_science": 16,
        "design": 8,
        "marketing": 6,
        "business": 8,
        "cloud": 10,
        "devops": 14,
        "ai_ml": 20,
        "web_dev": 12,
        "mobile_dev": 14,
        "cybersecurity": 16,
        "blockchain": 18,
        "game_dev": 16,
        "default": 12
    },
    "intermediate": {
        "programming": 8,
        "data_science": 12,
        "design": 6,
        "marketing": 4,
        "business": 6,
        "cloud": 8,
        "devops": 10,
        "ai_ml": 16,
        "web_dev": 8,
        "mobile_dev": 10,
        "cybersecurity": 12,
        "blockchain": 14,
        "game_dev": 12,
        "default": 8
    },
    "advanced": {
        "programming": 6,
        "data_science": 8,
        "design": 4,
        "marketing": 3,
        "business": 4,
        "cloud": 6,
        "devops": 8,
        "ai_ml": 12,
        "web_dev": 6,
        "mobile_dev": 8,
        "cybersecurity": 10,
        "blockchain": 12,
        "game_dev": 10,
        "default": 6
    }
}

# Resource types and platforms
RESOURCE_PLATFORMS = {
    "online_courses": ["Coursera", "Udemy", "edX", "Pluralsight", "LinkedIn Learning", "Udacity"],
    "documentation": ["Official Docs", "MDN", "W3Schools", "DevDocs"],
    "practice": ["LeetCode", "HackerRank", "CodeWars", "Exercism", "Kaggle"],
    "projects": ["GitHub", "Personal Portfolio", "Open Source", "Freelance"],
    "books": ["O'Reilly", "Manning", "Packt", "No Starch Press"],
    "community": ["Stack Overflow", "Reddit", "Discord", "Dev.to", "Medium"],
    "certifications": ["AWS", "Azure", "Google Cloud", "CompTIA", "Cisco"]
}

# Recommended YouTube channels by domain
YOUTUBE_CHANNELS = {
    "programming": ["freeCodeCamp", "Traversy Media", "Programming with Mosh", "The Net Ninja"],
    "data_science": ["StatQuest", "Krish Naik", "Ken Jee", "Data Science Dojo"],
    "design": ["Flux Academy", "The Futur", "Figma", "AJ&Smart"],
    "marketing": ["Neil Patel", "HubSpot", "Google Ads", "Think Media"],
    "business": ["Harvard Business Review", "Simon Sinek", "Gary Vaynerchuk"],
    "cloud": ["A Cloud Guru", "TechWorld with Nana", "freeCodeCamp AWS"],
    "devops": ["TechWorld with Nana", "DevOps Toolkit", "KodeKloud"],
    "ai_ml": ["Sentdex", "Two Minute Papers", "3Blue1Brown", "Yannic Kilcher"],
    "web_dev": ["Traversy Media", "Web Dev Simplified", "Fireship", "Kevin Powell"],
    "mobile_dev": ["Philipp Lackner", "Coding with Mitch", "Code with Chris"],
    "cybersecurity": ["NetworkChuck", "John Hammond", "The Cyber Mentor"],
    "blockchain": ["Dapp University", "EatTheBlocks", "Smart Contract Programmer"],
    "game_dev": ["Brackeys", "GameMaker", "Sebastian Lague", "Code Monkey"],
    "default": ["freeCodeCamp", "Traversy Media", "Fireship", "Programming with Mosh"]
}

# Career domain mapping
CAREER_DOMAINS = {
    "software_engineer": "programming",
    "data_scientist": "data_science",
    "data_analyst": "data_science",
    "ui_ux_designer": "design",
    "product_manager": "business",
    "digital_marketer": "marketing",
    "cloud_engineer": "cloud",
    "devops_engineer": "devops",
    "ml_engineer": "ai_ml",
    "web_developer": "web_dev",
    "mobile_developer": "mobile_dev",
    "cybersecurity": "cybersecurity",
    "blockchain_dev": "blockchain",
    "game_developer": "game_dev"
}


class RoadmapGenerator:
    """Generate personalized learning roadmaps with AI"""
    
    def __init__(self):
        self.llm = None
        try:
            if _settings.openai_api_key:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=_settings.openai_api_key
                )
        except Exception as e:
            print(f"Warning: Could not initialize ChatOpenAI: {e}")
        
    def generate_roadmap(
        self,
        career_goal: str,
        current_level: str = "beginner",
        time_commitment: str = "moderate",  # light, moderate, intensive
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete learning roadmap
        
        Args:
            career_goal: Target career or skill (e.g., "Data Scientist", "Python Developer")
            current_level: beginner, intermediate, advanced
            time_commitment: light (5h/week), moderate (10h/week), intensive (20h/week)
            preferences: Optional dict with learning_style, budget, etc.
        
        Returns:
            Complete roadmap with phases, milestones, resources, timeline
        """
        preferences = preferences or {}
        
        # Determine domain and timeline
        domain = self._get_domain(career_goal)
        total_weeks = self._calculate_timeline(domain, current_level, time_commitment)
        
        # Generate AI-powered roadmap structure
        roadmap_structure = self._generate_structure(career_goal, current_level, preferences)
        
        # Generate detailed phases with milestones
        phases = self._generate_phases(
            career_goal,
            current_level,
            roadmap_structure,
            total_weeks
        )
        
        # Add resources to each phase
        for phase in phases:
            phase["resources"] = self._generate_resources(
                phase["title"],
                phase["skills"],
                preferences.get("learning_style", "mixed"),
                preferences.get("budget", "free"),
                domain
            )
        
        return {
            "career_goal": career_goal,
            "current_level": current_level,
            "time_commitment": time_commitment,
            "total_duration_weeks": total_weeks,
            "estimated_completion": self._calculate_completion_date(total_weeks),
            "phases": phases,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "domain": domain,
                "total_phases": len(phases),
                "total_skills": sum(len(p["skills"]) for p in phases)
            }
        }
    
    def _get_domain(self, career_goal: str) -> str:
        """Map career goal to domain category"""
        career_lower = career_goal.lower().replace(" ", "_")
        
        # Direct match
        if career_lower in CAREER_DOMAINS:
            return CAREER_DOMAINS[career_lower]
        
        # Partial match
        for career_key, domain in CAREER_DOMAINS.items():
            if career_key in career_lower or career_lower in career_key:
                return domain
        
        # Keyword-based detection
        if any(kw in career_lower for kw in ["data", "analyst", "scientist", "ml", "machine"]):
            return "data_science"
        elif any(kw in career_lower for kw in ["web", "frontend", "backend", "fullstack"]):
            return "web_dev"
        elif any(kw in career_lower for kw in ["design", "ui", "ux", "graphic"]):
            return "design"
        elif any(kw in career_lower for kw in ["cloud", "aws", "azure", "gcp"]):
            return "cloud"
        elif any(kw in career_lower for kw in ["devops", "sre", "infrastructure"]):
            return "devops"
        
        return "default"
    
    def _calculate_timeline(self, domain: str, level: str, commitment: str) -> int:
        """Calculate total learning time in weeks"""
        base_weeks = SKILL_LEARNING_TIME.get(level, {}).get(domain, 12)
        
        # Adjust for time commitment
        if commitment == "light":
            return int(base_weeks * 1.5)  # 5 hours/week
        elif commitment == "intensive":
            return int(base_weeks * 0.7)  # 20 hours/week
        else:
            return base_weeks  # 10 hours/week (moderate)
    
    def _calculate_completion_date(self, weeks: int) -> str:
        """Calculate estimated completion date"""
        completion = datetime.now() + timedelta(weeks=weeks)
        return completion.strftime("%B %Y")
    
    def _generate_structure(
        self,
        career_goal: str,
        current_level: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use AI to generate roadmap structure"""
        prompt = f"""Generate a learning roadmap structure for someone who wants to become a {career_goal}.

Current Level: {current_level}
Learning Preferences: {preferences.get('learning_style', 'mixed')}

Create a structured learning path with 4-6 phases. Each phase should have:
1. A descriptive title
2. Core skills to learn in that phase
3. Key outcomes/competencies
4. Prerequisites (if any)

Return ONLY a JSON object with this structure:
{{
  "phases": [
    {{
      "title": "Foundation Phase",
      "duration_weeks": 4,
      "skills": ["skill1", "skill2"],
      "outcomes": ["outcome1", "outcome2"],
      "prerequisites": []
    }}
  ]
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert learning path designer. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            import json
            return json.loads(content)
            
        except Exception as e:
            print(f"Error generating structure: {e}")
            return self._get_fallback_structure(career_goal, current_level)
    
    def _get_fallback_structure(self, career_goal: str, level: str) -> Dict[str, Any]:
        """Fallback structure if AI generation fails"""
        if level == "beginner":
            return {
                "phases": [
                    {
                        "title": "Foundation & Basics",
                        "duration_weeks": 4,
                        "skills": ["Core concepts", "Basic tools", "Development environment"],
                        "outcomes": ["Understand fundamentals", "Setup workspace"],
                        "prerequisites": []
                    },
                    {
                        "title": "Intermediate Skills",
                        "duration_weeks": 6,
                        "skills": ["Advanced concepts", "Best practices", "Real projects"],
                        "outcomes": ["Build projects", "Write clean code"],
                        "prerequisites": ["Foundation & Basics"]
                    },
                    {
                        "title": "Advanced & Specialization",
                        "duration_weeks": 8,
                        "skills": ["Specialization", "System design", "Portfolio"],
                        "outcomes": ["Expert-level skills", "Job-ready portfolio"],
                        "prerequisites": ["Intermediate Skills"]
                    }
                ]
            }
        else:
            return {
                "phases": [
                    {
                        "title": "Skill Enhancement",
                        "duration_weeks": 6,
                        "skills": ["Advanced techniques", "Industry tools"],
                        "outcomes": ["Professional proficiency"],
                        "prerequisites": []
                    },
                    {
                        "title": "Specialization",
                        "duration_weeks": 8,
                        "skills": ["Domain expertise", "Advanced projects"],
                        "outcomes": ["Expert status", "Portfolio"],
                        "prerequisites": ["Skill Enhancement"]
                    }
                ]
            }
    
    def _generate_phases(
        self,
        career_goal: str,
        level: str,
        structure: Dict[str, Any],
        total_weeks: int
    ) -> List[Dict[str, Any]]:
        """Generate detailed phases from structure"""
        phases = []
        phases_data = structure.get("phases", [])
        
        # Distribute weeks across phases
        num_phases = len(phases_data)
        if num_phases == 0:
            return []
        
        weeks_per_phase = total_weeks // num_phases
        remaining_weeks = total_weeks % num_phases
        
        for idx, phase_data in enumerate(phases_data):
            duration = weeks_per_phase + (1 if idx < remaining_weeks else 0)
            
            phases.append({
                "phase_number": idx + 1,
                "title": phase_data.get("title", f"Phase {idx + 1}"),
                "duration_weeks": duration,
                "skills": phase_data.get("skills", []),
                "outcomes": phase_data.get("outcomes", []),
                "prerequisites": phase_data.get("prerequisites", []),
                "milestones": self._generate_milestones(
                    phase_data.get("skills", []),
                    duration
                ),
                "resources": []  # Will be filled later
            })
        
        return phases
    
    def _generate_milestones(self, skills: List[str], weeks: int) -> List[Dict[str, Any]]:
        """Generate milestones for a phase"""
        milestones = []
        
        if weeks <= 2:
            num_milestones = len(skills)
        elif weeks <= 6:
            num_milestones = min(len(skills) * 2, 8)
        else:
            num_milestones = min(len(skills) * 3, 12)
        
        weeks_per_milestone = weeks / max(num_milestones, 1)
        
        for i in range(min(num_milestones, len(skills) * 2)):
            skill_idx = i // 2 if i < len(skills) * 2 else i - len(skills)
            skill = skills[skill_idx % len(skills)]
            
            week_num = int((i + 1) * weeks_per_milestone)
            
            if i % 2 == 0:
                milestone_type = "Learn"
                description = f"Complete learning materials for {skill}"
            else:
                milestone_type = "Practice"
                description = f"Build project demonstrating {skill}"
            
            milestones.append({
                "week": min(week_num, weeks),
                "type": milestone_type,
                "title": f"{milestone_type}: {skill}",
                "description": description,
                "completed": False
            })
        
        return milestones
    
    def _generate_resources(
        self,
        phase_title: str,
        skills: List[str],
        learning_style: str,
        budget: str,
        domain: str
    ) -> List[Dict[str, Any]]:
        """Generate resources for a phase"""
        resources = []
        
        # Always include free resources
        resources.extend([
            {
                "type": "Documentation",
                "title": f"Official Documentation - {skills[0] if skills else 'Core Topics'}",
                "platform": "Official Docs",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            },
            {
                "type": "Practice",
                "title": "Hands-on Exercises & Challenges",
                "platform": "GitHub",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            }
        ])
        
        # Add video courses if preferred
        if learning_style in ["visual", "mixed"]:
            # Always add free YouTube tutorials
            resources.append({
                "type": "Video Tutorial",
                "title": f"{phase_title} - Free YouTube Playlist",
                "platform": "YouTube",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            })
            
            # Add paid premium courses if budget allows
            if budget == "paid":
                resources.append({
                    "type": "Premium Course",
                    "title": f"{phase_title} - Complete Certification",
                    "platform": "Coursera",
                    "url": "#",
                    "cost": "₹4,100",
                    "priority": "Medium"
                })
        
        # Add interactive practice
        if any(kw in phase_title.lower() for kw in ["coding", "programming", "development"]):
            # YouTube coding tutorials
            resources.append({
                "type": "Video Tutorial",
                "title": f"{phase_title} - Coding Tutorials & Walkthroughs",
                "platform": "YouTube",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            })
            
            # Practice platforms
            resources.append({
                "type": "Interactive Practice",
                "title": "Coding Challenges & Projects",
                "platform": "LeetCode" if budget == "paid" else "Exercism",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            })
        
        # Add books for readers
        if learning_style in ["reading", "mixed"]:
            # Add free YouTube video explanations
            resources.append({
                "type": "Video Tutorial",
                "title": f"{skills[0] if skills else 'Core Concepts'} - YouTube Tutorials",
                "platform": "YouTube",
                "url": "#",
                "cost": "Free",
                "priority": "High"
            })
            
            # Add paid books if budget allows
            if budget == "paid":
                resources.append({
                    "type": "Book",
                    "title": f"Mastering {skills[0] if skills else 'Core Concepts'}",
                    "platform": "O'Reilly",
                    "url": "#",
                    "cost": "₹3,200",
                    "priority": "Medium"
                })
        
        # Add community resources
        resources.append({
            "type": "Community",
            "title": "Discussion Forum & Support",
            "platform": "Reddit",
            "url": "#",
            "cost": "Free",
            "priority": "Low"
        })
        
        # Add recommended YouTube channels for this domain
        youtube_channels = YOUTUBE_CHANNELS.get(domain, YOUTUBE_CHANNELS["default"])
        recommended_channels = ", ".join(youtube_channels[:3])  # Top 3 channels
        resources.append({
            "type": "YouTube Channels",
            "title": f"Recommended: {recommended_channels}",
            "platform": "YouTube",
            "url": "#",
            "cost": "Free",
            "priority": "High"
        })
        
        return resources
    
    def update_milestone(
        self,
        roadmap: Dict[str, Any],
        phase_number: int,
        milestone_week: int,
        completed: bool
    ) -> Dict[str, Any]:
        """Update milestone completion status"""
        for phase in roadmap["phases"]:
            if phase["phase_number"] == phase_number:
                for milestone in phase["milestones"]:
                    if milestone["week"] == milestone_week:
                        milestone["completed"] = completed
                        break
        return roadmap
    
    def get_progress(self, roadmap: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate roadmap progress"""
        total_milestones = 0
        completed_milestones = 0
        
        for phase in roadmap["phases"]:
            for milestone in phase["milestones"]:
                total_milestones += 1
                if milestone.get("completed", False):
                    completed_milestones += 1
        
        progress_percent = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
        
        return {
            "total_milestones": total_milestones,
            "completed_milestones": completed_milestones,
            "progress_percent": round(progress_percent, 1),
            "phases_completed": sum(1 for p in roadmap["phases"] 
                                   if all(m.get("completed", False) for m in p["milestones"])),
            "current_phase": next(
                (p["phase_number"] for p in roadmap["phases"] 
                 if not all(m.get("completed", False) for m in p["milestones"])),
                len(roadmap["phases"])
            )
        }


# Global instance
roadmap_generator = RoadmapGenerator()
