"""
Experience Translator
Converts non-traditional experience into professional skills and resume bullets
"""

from typing import Dict, List
from openai import OpenAI
from config import get_settings
import json
import re

settings = get_settings()


def translate_experience(raw_experience: str) -> Dict:
    """
    Translate non-traditional experience into professional format.

    Input: free text like "Ran a YouTube channel with 10K subscribers"
    Output: skills, resume bullets, matching job roles
    """
    if not settings.openai_api_key:
        return _fallback_translation(raw_experience)

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = f"""You are a career advisor. A student describes a non-traditional experience below.
Translate it into professional terms.

Experience: "{raw_experience}"

Return ONLY valid JSON:
{{
  "professional_skills": ["list of 5-8 professional skills demonstrated"],
  "resume_bullets": [
    "3-4 professionally worded resume bullet points using action verbs and metrics where possible"
  ],
  "matching_roles": [
    {{
      "title": "Job title where these skills apply",
      "relevance": "One sentence explaining why"
    }}
  ],
  "skill_categories": {{
    "technical": ["list"],
    "soft": ["list"],
    "domain": ["list"]
  }}
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career advisor who translates life experience into professional value. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(content)
    except Exception as e:
        print(f"Experience translation failed: {e}")
        return _fallback_translation(raw_experience)


def _fallback_translation(raw_experience: str) -> Dict:
    """Fallback when AI is unavailable"""
    return {
        "professional_skills": ["Communication", "Self-Management", "Initiative", "Creativity"],
        "resume_bullets": [
            f"Demonstrated initiative by independently pursuing: {raw_experience[:80]}",
            "Developed key transferable skills through hands-on experience",
        ],
        "matching_roles": [
            {"title": "Project Coordinator", "relevance": "Self-directed projects show coordination skills"},
            {"title": "Content Creator", "relevance": "Creative experience translates to content roles"},
        ],
        "skill_categories": {
            "technical": [],
            "soft": ["Communication", "Self-Management", "Initiative"],
            "domain": ["Creative Problem Solving"],
        },
    }
