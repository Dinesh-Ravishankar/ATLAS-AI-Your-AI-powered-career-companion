"""
Project Recommendation System
Suggests career-aligned portfolio projects using GitHub API and AI
"""

import requests
from typing import List, Dict, Optional
from config import get_settings
from openai import OpenAI

settings = get_settings()


class ProjectRecommender:
    """Recommends portfolio projects based on skills and target roles"""
    
    def __init__(self):
        self.github_token = settings.github_token
        self.github_api_base = "https://api.github.com"
        self.openai_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    def recommend_projects(
        self, 
        skills: List[str], 
        target_role: str, 
        difficulty: str = "beginner",
        count: int = 5
    ) -> List[Dict]:
        """
        Recommend projects based on user's skills and target career
        
        Args:
            skills: List of user's current skills
            target_role: Target career/job title
            difficulty: Project difficulty level (beginner, intermediate, advanced)
            count: Number of recommendations to return
        
        Returns:
            List of project recommendations with details
        """
        recommendations = []
        
        # Strategy 1: AI-generated custom project ideas
        if self.openai_client:
            ai_projects = self._generate_ai_project_ideas(skills, target_role, difficulty, count=3)
            recommendations.extend(ai_projects)
        
        # Strategy 2: GitHub trending repositories
        github_projects = self._fetch_github_projects(target_role, difficulty, count=3)
        recommendations.extend(github_projects)
        
        # Deduplicate and limit to requested count
        unique_projects = self._deduplicate_projects(recommendations)
        return unique_projects[:count]
    
    def _generate_ai_project_ideas(
        self, 
        skills: List[str], 
        target_role: str, 
        difficulty: str,
        count: int = 3
    ) -> List[Dict]:
        """Generate custom project ideas using OpenAI"""
        try:
            skills_str = ", ".join(skills) if skills else "general programming"
            
            prompt = f"""You are a career advisor helping a student build a portfolio for a {target_role} role.

Current Skills: {skills_str}
Difficulty Level: {difficulty}

Generate {count} portfolio project ideas that would:
1. Showcase relevant skills for {target_role}
2. Be achievable at {difficulty} level
3. Impress potential employers
4. Build upon existing skills: {skills_str}

For each project, provide:
- Project title (creative and professional)
- Brief description (2 sentences)
- Key technologies to use (3-5 items)
- Estimated time to complete (in hours)
- Why it's valuable for this career path

Format as JSON array with keys: title, description, technologies, time_estimate, value_proposition"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a career advisor specializing in portfolio development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON from response
            import json
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                projects = json.loads(json_match.group())
                # Add source and format
                for project in projects:
                    project['source'] = 'AI Generated'
                    project['source_type'] = 'custom'
                    project['difficulty'] = difficulty
                return projects
            
        except Exception as e:
            print(f"AI project generation error: {e}")
        
        # Fallback to curated project ideas
        return self._get_fallback_projects(target_role, difficulty, count)
    
    def _fetch_github_projects(
        self, 
        target_role: str, 
        difficulty: str,
        count: int = 3
    ) -> List[Dict]:
        """Fetch relevant projects from GitHub"""
        try:
            # Build search query based on role and difficulty
            search_terms = self._get_search_terms(target_role, difficulty)
            
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            projects = []
            for term in search_terms[:2]:  # Search top 2 relevant terms
                url = f"{self.github_api_base}/search/repositories"
                params = {
                    'q': f'{term} {difficulty} tutorial OR project',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 3
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    repos = response.json().get('items', [])
                    for repo in repos[:2]:  # Take top 2 from each search
                        projects.append({
                            'title': repo['name'].replace('-', ' ').title(),
                            'description': repo.get('description', 'No description available'),
                            'technologies': [repo.get('language', 'Multiple')],
                            'time_estimate': self._estimate_project_time(difficulty),
                            'value_proposition': f"Learn from a popular open-source project with {repo['stargazers_count']} stars",
                            'source': 'GitHub',
                            'source_type': 'repository',
                            'url': repo['html_url'],
                            'stars': repo['stargazers_count'],
                            'difficulty': difficulty
                        })
            
            return projects[:count]
            
        except Exception as e:
            print(f"GitHub API error: {e}")
            return []
    
    def _get_search_terms(self, target_role: str, difficulty: str) -> List[str]:
        """Generate search terms based on target role"""
        role_terms = {
            'software engineer': ['web-app', 'rest-api', 'full-stack'],
            'data scientist': ['machine-learning', 'data-analysis', 'python-data'],
            'frontend developer': ['react', 'vue', 'frontend'],
            'backend developer': ['nodejs', 'python-backend', 'api'],
            'mobile developer': ['react-native', 'flutter', 'mobile-app'],
            'devops': ['docker', 'kubernetes', 'ci-cd'],
            'data analyst': ['data-visualization', 'sql', 'dashboard'],
            'machine learning engineer': ['deep-learning', 'neural-network', 'ml-model']
        }
        
        # Get terms for role or use generic terms
        role_key = target_role.lower()
        for key in role_terms:
            if key in role_key:
                return role_terms[key]
        
        return ['full-stack', 'web-app', 'api']
    
    def _estimate_project_time(self, difficulty: str) -> str:
        """Estimate time to complete based on difficulty"""
        time_estimates = {
            'beginner': '10-20 hours',
            'intermediate': '30-50 hours',
            'advanced': '60-100 hours'
        }
        return time_estimates.get(difficulty, '20-40 hours')
    
    def _get_fallback_projects(self, target_role: str, difficulty: str, count: int) -> List[Dict]:
        """Curated fallback project ideas when AI/API fails"""
        all_projects = {
            'software engineer': [
                {
                    'title': 'Personal Portfolio Website',
                    'description': 'Build a responsive portfolio showcasing your projects, skills, and resume. Include dark mode and animations.',
                    'technologies': ['React', 'Tailwind CSS', 'Vercel'],
                    'time_estimate': '15-25 hours',
                    'value_proposition': 'Essential for any developer - shows both technical and design skills',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Task Management API',
                    'description': 'Create a RESTful API for a todo/task management system with user authentication and CRUD operations.',
                    'technologies': ['FastAPI', 'PostgreSQL', 'JWT'],
                    'time_estimate': '20-30 hours',
                    'value_proposition': 'Demonstrates backend skills and understanding of API design',
                    'difficulty': 'intermediate'
                },
                {
                    'title': 'Real-time Chat Application',
                    'description': 'Build a scalable chat app with WebSockets, user presence, typing indicators, and message history.',
                    'technologies': ['Node.js', 'Socket.io', 'Redis', 'React'],
                    'time_estimate': '40-60 hours',
                    'value_proposition': 'Shows understanding of real-time systems and scalability',
                    'difficulty': 'advanced'
                }
            ],
            'data scientist': [
                {
                    'title': 'Exploratory Data Analysis Dashboard',
                    'description': 'Create an interactive dashboard analyzing a public dataset with visualizations and insights.',
                    'technologies': ['Python', 'Pandas', 'Plotly', 'Streamlit'],
                    'time_estimate': '15-25 hours',
                    'value_proposition': 'Demonstrates data wrangling and visualization skills',
                    'difficulty': 'beginner'
                },
                {
                    'title': 'Predictive Model for Business Problem',
                    'description': 'Build and deploy a machine learning model to predict customer churn, house prices, or stock trends.',
                    'technologies': ['Scikit-learn', 'XGBoost', 'Flask', 'Docker'],
                    'time_estimate': '35-50 hours',
                    'value_proposition': 'Shows end-to-end ML pipeline from data to deployment',
                    'difficulty': 'intermediate'
                }
            ],
            'generic': [
                {
                    'title': 'CRUD Application',
                    'description': 'Build a full-stack application with create, read, update, and delete functionality.',
                    'technologies': ['Your preferred stack'],
                    'time_estimate': '20-30 hours',
                    'value_proposition': 'Fundamental skill for most developer roles',
                    'difficulty': difficulty
                }
            ]
        }
        
        # Get projects for role or use generic
        role_key = 'generic'
        for key in all_projects:
            if key in target_role.lower():
                role_key = key
                break
        
        projects = all_projects.get(role_key, all_projects['generic'])
        
        # Filter by difficulty if possible
        filtered = [p for p in projects if p.get('difficulty') == difficulty]
        if not filtered:
            filtered = projects
        
        # Add source info
        for project in filtered:
            project['source'] = 'Curated'
            project['source_type'] = 'template'
        
        return filtered[:count]
    
    def _deduplicate_projects(self, projects: List[Dict]) -> List[Dict]:
        """Remove duplicate projects based on title similarity"""
        seen_titles = set()
        unique_projects = []
        
        for project in projects:
            title_key = project['title'].lower().replace(' ', '')
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_projects.append(project)
        
        return unique_projects


# Global instance
recommender = ProjectRecommender()


def get_project_recommendations(
    skills: List[str], 
    target_role: str, 
    difficulty: str = "beginner",
    count: int = 5
) -> List[Dict]:
    """Main function to get project recommendations"""
    return recommender.recommend_projects(skills, target_role, difficulty, count)
