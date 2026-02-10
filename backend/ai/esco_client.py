"""
ESCO API Client
Fetches occupation and skill data from the European Skills/Competences, 
Qualifications and Occupations (ESCO) classification API.
"""

import requests
from typing import List, Dict, Optional
from functools import lru_cache
from config import get_settings

settings = get_settings()

ESCO_BASE_URL = settings.esco_api_url or "https://ec.europa.eu/esco/api"


class ESCOClient:
    """Client for the ESCO API v1"""

    def __init__(self):
        self.base_url = ESCO_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Accept-Language": "en"
        })

    def search_occupations(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for occupations matching a query string"""
        try:
            resp = self.session.get(
                f"{self.base_url}/search",
                params={
                    "text": query,
                    "type": "occupation",
                    "language": "en",
                    "limit": limit,
                    "full": "false"
                },
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("_embedded", {}).get("results", []):
                results.append({
                    "uri": item.get("uri", ""),
                    "title": item.get("title", ""),
                    "description": item.get("description", "")[:200] if item.get("description") else "",
                })
            return results
        except Exception as e:
            print(f"ESCO search error: {e}")
            return []

    def get_occupation_skills(self, occupation_uri: str) -> Dict[str, List[str]]:
        """Get essential and optional skills for an occupation URI"""
        try:
            resp = self.session.get(
                f"{self.base_url}/resource/occupation",
                params={"uri": occupation_uri, "language": "en"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()

            essential = []
            optional = []

            # Extract skills from _links
            links = data.get("_links", {})
            for rel_type, skill_list_key in [
                ("hasEssentialSkill", essential),
                ("hasOptionalSkill", optional),
            ]:
                items = links.get(rel_type, [])
                if isinstance(items, dict):
                    items = [items]
                for item in items:
                    title = item.get("title", item.get("skillType", ""))
                    if title:
                        skill_list_key.append(title)

            return {
                "title": data.get("title", ""),
                "essential_skills": essential[:15],
                "optional_skills": optional[:10],
                "description": (data.get("description", {}).get("en", {}).get("literal", "") or "")[:300]
            }
        except Exception as e:
            print(f"ESCO occupation detail error: {e}")
            return {"title": "", "essential_skills": [], "optional_skills": [], "description": ""}

    def get_skills_for_role(self, role_name: str) -> Dict[str, List[str]]:
        """Convenience: search for a role and get its skills"""
        occupations = self.search_occupations(role_name, limit=1)
        if not occupations:
            return {"title": role_name, "essential_skills": [], "optional_skills": [], "description": ""}

        uri = occupations[0]["uri"]
        return self.get_occupation_skills(uri)


# Global singleton
esco_client = ESCOClient()


@lru_cache(maxsize=50)
def get_role_skills_cached(role_name: str) -> tuple:
    """Cached wrapper for role skill lookups. Returns (essential, optional) tuples."""
    data = esco_client.get_skills_for_role(role_name)
    return tuple(data.get("essential_skills", [])), tuple(data.get("optional_skills", []))
