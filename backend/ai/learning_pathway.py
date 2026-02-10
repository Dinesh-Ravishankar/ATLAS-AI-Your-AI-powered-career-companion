"""
Learning Pathway Generator
Creates personalized learning roadmaps for bridging skill gaps
"""

from typing import Dict, List
from openai import OpenAI
from config import get_settings
import json
import re

settings = get_settings()


def generate_learning_path(
    missing_skills: List[str],
    target_role: str,
    current_level: str = "beginner",
    weekly_hours: int = 10,
) -> List[Dict]:
    """
    Generate a step-by-step learning path for missing skills.
    
    Returns list of learning steps with resources.
    """
    if not settings.openai_api_key:
        return _fallback_path(missing_skills, target_role)

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = f"""Create a personalized learning roadmap for a student targeting a {target_role} role.

Missing skills to learn: {', '.join(missing_skills[:8])}
Current level: {current_level}
Available time: {weekly_hours} hours/week

For each skill, provide a learning step. Return ONLY a JSON array:
[
  {{
    "skill": "Skill name",
    "priority": "high/medium/low",
    "estimated_weeks": number,
    "resources": [
      {{
        "title": "Course/resource name",
        "platform": "Coursera/Udemy/YouTube/FreeCodeCamp/etc",
        "type": "course/tutorial/book/project",
        "url": "https://example.com or #",
        "free": true/false
      }}
    ],
    "milestone": "What you can do after completing this step",
    "practice_project": "A small hands-on project to solidify learning"
  }}
]

Order by priority (high first). Limit to {min(len(missing_skills), 8)} steps."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a learning path advisor. Return only valid JSON arrays."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(content)
    except Exception as e:
        print(f"Learning path generation failed: {e}")
        return _fallback_path(missing_skills, target_role)


def _fallback_path(missing_skills: List[str], target_role: str) -> List[Dict]:
    """Fallback learning path when AI is unavailable"""
    steps = []
    for i, skill in enumerate(missing_skills[:6]):
        steps.append({
            "skill": skill,
            "priority": "high" if i < 2 else ("medium" if i < 4 else "low"),
            "estimated_weeks": 3 + i,
            "resources": [
                {
                    "title": f"Learn {skill} - Complete Guide",
                    "platform": "Coursera",
                    "type": "course",
                    "url": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}",
                    "free": False,
                },
                {
                    "title": f"{skill} Tutorial",
                    "platform": "YouTube",
                    "type": "tutorial",
                    "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial",
                    "free": True,
                },
            ],
            "milestone": f"Able to apply {skill} in real projects",
            "practice_project": f"Build a small project demonstrating {skill} for {target_role}",
        })
    return steps
