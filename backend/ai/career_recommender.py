from typing import List
from models.schemas import CareerRecommendation
import random

class CareerRecommender:
    def __init__(self):
        # Mock career database
        self.careers = [
            {
                "title": "Data Scientist",
                "description": "Analyze complex data to help companies make decisions",
                "required_skills": ["Python", "Statistics", "Machine Learning", "SQL"],
                "average_salary": 120000,
                "growth_rate": 35.0,
                "keywords": ["data", "analytics", "math", "statistics", "python"]
            },
            {
                "title": "Software Engineer",
                "description": "Design, develop, and maintain software applications",
                "required_skills": ["Programming", "Algorithms", "Data Structures", "Git"],
                "average_salary": 110000,
                "growth_rate": 22.0,
                "keywords": ["coding", "programming", "software", "development", "tech"]
            },
            {
                "title": "Product Manager",
                "description": "Define product vision and strategy",
                "required_skills": ["Communication", "Strategy", "Data Analysis", "Leadership"],
                "average_salary": 130000,
                "growth_rate": 18.0,
                "keywords": ["product", "strategy", "management", "business", "leadership"]
            },
            {
                "title": "UX Designer",
                "description": "Create user-centered designs for digital products",
                "required_skills": ["Figma", "User Research", "Prototyping", "Design Thinking"],
                "average_salary": 95000,
                "growth_rate": 24.0,
                "keywords": ["design", "user experience", "creative", "visual", "interface"]
            },
            {
                "title": "DevOps Engineer",
                "description": "Automate and optimize software deployment",
                "required_skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "Cloud"],
                "average_salary": 115000,
                "growth_rate": 28.0,
                "keywords": ["automation", "infrastructure", "cloud", "deployment", "systems"]
            }
        ]
    
    def recommend(
        self,
        user_skills: List[str],
        interests: List[str],
        academic_performance: float = 3.0
    ) -> List[CareerRecommendation]:
        recommendations = []
        
        for career in self.careers:
            # Calculate match score
            skill_match = self._calculate_skill_match(user_skills, career["required_skills"])
            interest_match = self._calculate_interest_match(interests, career["keywords"])
            
            # Weighted score
            match_score = (skill_match * 0.6) + (interest_match * 0.4)
            
            # Generate reasons
            reasons = self._generate_reasons(user_skills, interests, career, skill_match, interest_match)
            
            recommendations.append(CareerRecommendation(
                title=career["title"],
                match_score=round(match_score, 2),
                description=career["description"],
                required_skills=career["required_skills"],
                average_salary=career["average_salary"],
                growth_rate=career["growth_rate"],
                reasons=reasons
            ))
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:5]
    
    def _calculate_skill_match(self, user_skills: List[str], required_skills: List[str]) -> float:
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        matches = sum(1 for skill in required_skills_lower if any(us in skill or skill in us for us in user_skills_lower))
        return (matches / len(required_skills) * 100) if required_skills else 0
    
    def _calculate_interest_match(self, interests: List[str], keywords: List[str]) -> float:
        if not interests:
            return 50.0  # Neutral score
        
        interests_lower = [i.lower() for i in interests]
        matches = sum(1 for keyword in keywords if any(interest in keyword or keyword in interest for interest in interests_lower))
        return (matches / len(keywords) * 100) if keywords else 0
    
    def _generate_reasons(self, user_skills, interests, career, skill_match, interest_match) -> List[str]:
        reasons = []
        
        if skill_match > 50:
            reasons.append(f"Your skills align well with {career['title']} requirements ({skill_match:.0f}% match)")
        
        if interest_match > 50:
            reasons.append(f"Your interests match this career path ({interest_match:.0f}% match)")
        
        if career["growth_rate"] > 20:
            reasons.append(f"High growth industry ({career['growth_rate']}% projected growth)")
        
        if career["average_salary"] > 100000:
            reasons.append(f"Competitive salary (${career['average_salary']:,} average)")
        
        return reasons[:3]
