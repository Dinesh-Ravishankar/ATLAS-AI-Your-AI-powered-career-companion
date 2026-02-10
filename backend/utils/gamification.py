"""
Gamification Utilities
XP awards, badge checks, level calculation
"""

from typing import Dict, List, Optional


# XP costs for actions
XP_ACTIONS = {
    "complete_profile": 100,
    "upload_resume": 150,
    "take_career_quiz": 200,
    "run_skill_gap": 150,
    "verify_job": 100,
    "add_project": 120,
    "complete_learning_step": 80,
    "github_import": 200,
    "complete_onboarding": 300,
    "daily_login": 25,
    "chat_with_atlas": 50,
    "mock_interview": 250,
    "translate_experience": 150,
}

# Level thresholds
LEVELS = [
    {"level": 1, "name": "Explorer", "min_xp": 0},
    {"level": 2, "name": "Learner", "min_xp": 200},
    {"level": 3, "name": "Builder", "min_xp": 500},
    {"level": 4, "name": "Achiever", "min_xp": 1000},
    {"level": 5, "name": "Expert", "min_xp": 2000},
    {"level": 6, "name": "Master", "min_xp": 3500},
    {"level": 7, "name": "Legend", "min_xp": 5000},
]

# Badge definitions
BADGES = {
    "profile_complete": {
        "name": "Profile Pro",
        "description": "Completed your full profile",
        "icon": "👤",
        "condition": "complete_profile",
    },
    "first_quiz": {
        "name": "Quiz Starter",
        "description": "Took your first career quiz",
        "icon": "🧠",
        "condition": "take_career_quiz",
    },
    "skill_scanner": {
        "name": "Skill Scanner",
        "description": "Ran your first skill gap analysis",
        "icon": "🔍",
        "condition": "run_skill_gap",
    },
    "ghost_buster": {
        "name": "Ghost Buster",
        "description": "Verified a job posting",
        "icon": "👻",
        "condition": "verify_job",
    },
    "builder": {
        "name": "Builder",
        "description": "Added 3 projects to your portfolio",
        "icon": "🏗️",
        "condition": "projects_3",
    },
    "github_connected": {
        "name": "Connected",
        "description": "Imported skills from GitHub",
        "icon": "🔗",
        "condition": "github_import",
    },
    "level_5": {
        "name": "Expert Status",
        "description": "Reached Level 5",
        "icon": "⭐",
        "condition": "reach_level_5",
    },
    "interview_ready": {
        "name": "Interview Ready",
        "description": "Completed a mock interview",
        "icon": "🎤",
        "condition": "mock_interview",
    },
}


def calculate_xp_for_action(action: str) -> int:
    """Get XP reward for an action"""
    return XP_ACTIONS.get(action, 0)


def get_level(total_xp: int) -> Dict:
    """Get current level based on total XP"""
    current_level = LEVELS[0]
    for level in LEVELS:
        if total_xp >= level["min_xp"]:
            current_level = level
        else:
            break

    # Calculate progress to next level
    current_idx = LEVELS.index(current_level)
    if current_idx < len(LEVELS) - 1:
        next_level = LEVELS[current_idx + 1]
        progress = (total_xp - current_level["min_xp"]) / (next_level["min_xp"] - current_level["min_xp"])
        xp_to_next = next_level["min_xp"] - total_xp
    else:
        progress = 1.0
        xp_to_next = 0

    return {
        **current_level,
        "total_xp": total_xp,
        "progress_to_next": round(min(progress, 1.0), 2),
        "xp_to_next_level": max(xp_to_next, 0),
    }


def check_badges(user_actions: Dict) -> List[Dict]:
    """Check which badges user has earned based on their actions"""
    earned = []
    for badge_id, badge in BADGES.items():
        condition = badge["condition"]
        if condition in user_actions and user_actions[condition]:
            earned.append({
                "id": badge_id,
                "name": badge["name"],
                "description": badge["description"],
                "icon": badge["icon"],
                "earned": True,
            })
    return earned


def get_all_badges(user_actions: Dict) -> List[Dict]:
    """Get all badges with earned status"""
    all_badges = []
    for badge_id, badge in BADGES.items():
        condition = badge["condition"]
        earned = condition in user_actions and user_actions[condition]
        all_badges.append({
            "id": badge_id,
            "name": badge["name"],
            "description": badge["description"],
            "icon": badge["icon"],
            "earned": earned,
        })
    return all_badges


def get_gamification_summary(total_xp: int, user_actions: Dict) -> Dict:
    """Get full gamification summary for a user"""
    level_info = get_level(total_xp)
    badges = get_all_badges(user_actions)
    earned_count = len([b for b in badges if b["earned"]])

    return {
        "level": level_info,
        "badges": badges,
        "badges_earned": earned_count,
        "badges_total": len(BADGES),
        "stats": {
            "total_xp": total_xp,
            "actions_completed": sum(1 for v in user_actions.values() if v),
        },
    }
