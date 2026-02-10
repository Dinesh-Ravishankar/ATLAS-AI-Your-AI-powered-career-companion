from typing import List, Dict, Optional
import numpy as np
from models.schemas import SkillGapAnalysis

class SkillGapAnalyzer:
    def __init__(self):
        self._embedder: Optional[any] = None
        
        # Mock data for demo (replace with ESCO/O*NET API calls)
        self.role_skills = {
            "Data Scientist": [
                "Python", "Machine Learning", "Statistics", "SQL", "Data Visualization",
                "Deep Learning", "Pandas", "NumPy", "Scikit-learn", "TensorFlow"
            ],
            "Software Engineer": [
                "JavaScript", "Python", "Git", "REST APIs", "Database Design",
                "React", "Node.js", "Docker", "Testing", "Agile"
            ],
            "Product Manager": [
                "Product Strategy", "User Research", "Data Analysis", "Communication",
                "Roadmap Planning", "Stakeholder Management", "Agile", "SQL", "A/B Testing"
            ],
            "UX Designer": [
                "Figma", "User Research", "Prototyping", "Wireframing", "Design Systems",
                "Usability Testing", "Adobe XD", "Sketch", "HTML/CSS", "Interaction Design"
            ]
        }
    
    @property
    def embedder(self):
        """Lazy-load the sentence transformer model only when needed"""
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"Warning: Could not load SentenceTransformer model: {e}")
                print("Skill gap analysis will use basic string matching instead.")
                self._embedder = False  # Mark as failed to avoid retrying
        return self._embedder if self._embedder is not False else None
    
    def analyze_gap(self, user_skills: List[str], target_role: str) -> SkillGapAnalysis:
        # Get required skills for role
        required_skills = self.role_skills.get(target_role, [])
        
        # Normalize skill names (lowercase, strip)
        user_skills_normalized = [s.lower().strip() for s in user_skills]
        required_skills_normalized = [s.lower().strip() for s in required_skills]
        
        # Find missing skills
        missing = []
        for skill in required_skills:
            if skill.lower().strip() not in user_skills_normalized:
                missing.append({
                    "name": skill,
                    "priority": "high" if skill in required_skills[:5] else "medium",
                    "time_to_learn": self._estimate_learning_time(skill)
                })
        
        # Calculate match percentage
        match_count = len(required_skills) - len(missing)
        match_percentage = (match_count / len(required_skills) * 100) if required_skills else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(missing[:3])
        
        return SkillGapAnalysis(
            target_role=target_role,
            current_skills=user_skills,
            required_skills=required_skills,
            missing_skills=missing,
            match_percentage=round(match_percentage, 2),
            recommendations=recommendations
        )
    
    def _estimate_learning_time(self, skill: str) -> str:
        # Simple heuristic
        if any(keyword in skill.lower() for keyword in ['deep learning', 'machine learning', 'tensorflow']):
            return "3-6 months"
        elif any(keyword in skill.lower() for keyword in ['python', 'javascript', 'sql']):
            return "2-4 months"
        else:
            return "1-2 months"
    
    def _generate_recommendations(self, top_missing: List[Dict]) -> List[str]:
        recommendations = []
        for skill in top_missing:
            recommendations.append(
                f"Learn {skill['name']} through online courses (Coursera, Udemy) - Est. {skill['time_to_learn']}"
            )
        return recommendations
