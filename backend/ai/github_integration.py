"""
GitHub Integration
Import skills and projects from GitHub profile/repos
"""

import httpx
from typing import Dict, List, Optional
import json
import re

GITHUB_API = "https://api.github.com"

# Language to skill mapping
LANGUAGE_SKILLS = {
    "Python": ["Python", "Backend Development"],
    "JavaScript": ["JavaScript", "Web Development"],
    "TypeScript": ["TypeScript", "Web Development"],
    "Java": ["Java", "Object-Oriented Programming"],
    "C++": ["C++", "Systems Programming"],
    "C#": ["C#", ".NET Development"],
    "Go": ["Go", "Backend Development"],
    "Rust": ["Rust", "Systems Programming"],
    "Ruby": ["Ruby", "Web Development"],
    "PHP": ["PHP", "Web Development"],
    "Swift": ["Swift", "iOS Development"],
    "Kotlin": ["Kotlin", "Android Development"],
    "R": ["R", "Data Analysis", "Statistics"],
    "Jupyter Notebook": ["Python", "Data Science"],
    "HTML": ["HTML", "Frontend Development"],
    "CSS": ["CSS", "Frontend Development"],
    "Shell": ["Shell Scripting", "DevOps"],
    "Dockerfile": ["Docker", "DevOps"],
    "HCL": ["Terraform", "Infrastructure as Code"],
}

# Topic/keyword to skill mapping
TOPIC_SKILLS = {
    "machine-learning": "Machine Learning",
    "deep-learning": "Deep Learning",
    "data-science": "Data Science",
    "web-development": "Web Development",
    "react": "React",
    "nextjs": "Next.js",
    "vue": "Vue.js",
    "angular": "Angular",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "Google Cloud",
    "devops": "DevOps",
    "api": "API Development",
    "database": "Database Management",
    "testing": "Software Testing",
    "ci-cd": "CI/CD",
    "blockchain": "Blockchain",
    "mobile": "Mobile Development",
}


async def fetch_github_profile(username: str) -> Optional[Dict]:
    """Fetch GitHub user profile and repos"""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            user_resp = await client.get(
                f"{GITHUB_API}/users/{username}",
                headers={"Accept": "application/vnd.github.v3+json"},
            )
            if user_resp.status_code != 200:
                return None

            user_data = user_resp.json()

            repos_resp = await client.get(
                f"{GITHUB_API}/users/{username}/repos",
                params={"sort": "updated", "per_page": 30},
                headers={"Accept": "application/vnd.github.v3+json"},
            )
            repos = repos_resp.json() if repos_resp.status_code == 200 else []

            return {
                "profile": {
                    "name": user_data.get("name", username),
                    "bio": user_data.get("bio", ""),
                    "public_repos": user_data.get("public_repos", 0),
                    "followers": user_data.get("followers", 0),
                    "avatar_url": user_data.get("avatar_url", ""),
                },
                "repos": repos,
            }
    except Exception as e:
        print(f"GitHub fetch error: {e}")
        return None


def extract_skills_from_repos(repos: List[Dict]) -> Dict:
    """Extract skills from GitHub repositories"""
    skills = set()
    languages = {}
    projects = []

    for repo in repos:
        if repo.get("fork"):
            continue

        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
            if lang in LANGUAGE_SKILLS:
                skills.update(LANGUAGE_SKILLS[lang])

        topics = repo.get("topics", [])
        for topic in topics:
            if topic in TOPIC_SKILLS:
                skills.add(TOPIC_SKILLS[topic])

        desc = (repo.get("description") or "").lower()
        for keyword, skill in TOPIC_SKILLS.items():
            if keyword.replace("-", " ") in desc or keyword in desc:
                skills.add(skill)

        if repo.get("stargazers_count", 0) > 0 or not repo.get("fork"):
            projects.append({
                "name": repo["name"],
                "description": repo.get("description", ""),
                "language": lang,
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
                "topics": topics,
            })

    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "skills": sorted(list(skills)),
        "top_languages": [{"language": l, "repos": c} for l, c in top_languages],
        "projects": projects[:15],
        "total_repos_analyzed": len([r for r in repos if not r.get("fork")]),
    }


async def import_github_skills(username: str) -> Optional[Dict]:
    """Main function: fetch GitHub profile and extract skills"""
    data = await fetch_github_profile(username)
    if not data:
        return None

    extracted = extract_skills_from_repos(data["repos"])
    return {
        "profile": data["profile"],
        **extracted,
    }
