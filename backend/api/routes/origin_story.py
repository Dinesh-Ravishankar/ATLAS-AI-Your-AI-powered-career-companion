"""
"The Origin Story" — Intelligent Stream & Major Selector
Reverse-engineers the future: asks what problems you want to solve,
filters by anti-tags, scores via Ikigai engine, returns personalised
stream recommendations with "Day in the Life" + "Reality Check".
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from config import get_db, get_settings
from models.database import User
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/origin-story", tags=["Origin Story"])

settings = get_settings()

# ═══════════════════════════════════════════════════════════
# 1. STREAM DATABASE  — metadata for every major
# ═══════════════════════════════════════════════════════════

STREAMS: Dict[str, Dict[str, Any]] = {
    "computer_science": {
        "name": "Computer Science",
        "emoji": "💻",
        "category": "Engineering",
        "required_tags": ["logic", "math", "problem_solving", "technology", "sitting"],
        "anti_tags": ["outdoors", "physical_labor", "blood", "animals"],
        "weights": {"math": 0.4, "physics": 0.2, "logic": 0.4},
        "subjects": ["Data Structures", "Algorithms", "Databases", "AI/ML", "Web Dev"],
        "careers": ["Software Engineer", "Data Scientist", "Product Manager", "ML Engineer"],
        "salary_range": "$70,000 - $180,000",
        "job_growth": "25% (Much faster than average)",
        "difficulty": 7,
        "dropout_rate": "20%",
        "work_life_balance": 7,
        "day_in_life": "☕ 9AM — Stand-up meeting with your team. You discuss a bug in the payment system.\n💻 10AM — Deep work: you write Python code to fix the bug and add a new feature.\n🍕 12PM — Lunch + tech talk on AI from a colleague.\n🤝 2PM — Code review: a teammate found a smarter solution and you learn something new.\n🧪 4PM — Testing & deployment. Your code goes live to 50,000 users.\n🎮 6PM — Home. You tinker with a side project — a game built with Unity.",
        "reality_check": {
            "math_required": True,
            "message": "CS requires strong logic and discrete math. If math isn't your strength, you'll need extra effort in Years 1-2. But many successful developers weren't math prodigies — persistence matters more than innate talent.",
        },
        "roadmap": ["Year 1: Programming fundamentals + Math", "Year 2: Data Structures & Algorithms", "Year 3: Specialization (AI/Web/Systems)", "Year 4: Internship + Capstone Project", "Job: Junior Software Engineer → Senior → Tech Lead"],
        "bridge_courses": ["Intro to Python (freeCodeCamp)", "CS50 by Harvard (free)", "Discrete Math (Khan Academy)"],
    },
    "mechanical_engineering": {
        "name": "Mechanical Engineering",
        "emoji": "⚙️",
        "category": "Engineering",
        "required_tags": ["physics", "math", "hands_on", "building", "problem_solving"],
        "anti_tags": ["sitting_all_day", "coding_heavy", "blood"],
        "weights": {"math": 0.35, "physics": 0.45, "logic": 0.2},
        "subjects": ["Thermodynamics", "Fluid Mechanics", "CAD/CAM", "Materials Science", "Robotics"],
        "careers": ["Design Engineer", "Manufacturing Engineer", "Automotive Engineer", "Robotics Engineer"],
        "salary_range": "$60,000 - $140,000",
        "job_growth": "10% (Average)",
        "difficulty": 8,
        "dropout_rate": "25%",
        "work_life_balance": 6,
        "day_in_life": "🏭 8AM — Arrive at the manufacturing plant. Safety briefing.\n📐 9AM — Work on CAD models for a new drone part using SolidWorks.\n🔧 11AM — Visit the shop floor to test a prototype. It didn't fit — back to redesign.\n🍽️ 1PM — Lunch with the testing team.\n📊 2PM — Stress analysis simulation on your computer.\n🤝 4PM — Meeting with the client to present your design progress.\n🏠 6PM — Head home. You 3D-print a phone stand as a hobby.",
        "reality_check": {
            "math_required": True,
            "message": "Mech Eng is one of the toughest engineering branches. Thermodynamics and Fluid Mechanics are notoriously difficult. But if you love building tangible things and seeing your designs come to life, the satisfaction is unmatched.",
        },
        "roadmap": ["Year 1: Engineering Math + Physics", "Year 2: Thermodynamics & Materials", "Year 3: CAD/CAM & Specialization", "Year 4: Industry Internship + Thesis", "Job: Junior Design Engineer → Senior → Lead"],
        "bridge_courses": ["Engineering Drawing Basics", "Intro to SolidWorks (YouTube)", "Physics Refresh (Khan Academy)"],
    },
    "medicine": {
        "name": "Medicine (MBBS/MD)",
        "emoji": "🩺",
        "category": "Health Sciences",
        "required_tags": ["biology", "chemistry", "empathy", "long_hours", "helping_people"],
        "anti_tags": ["blood_phobia", "impatient", "hate_memorizing"],
        "weights": {"biology": 0.5, "chemistry": 0.3, "empathy": 0.2},
        "subjects": ["Anatomy", "Physiology", "Pharmacology", "Pathology", "Surgery"],
        "careers": ["Doctor", "Surgeon", "Psychiatrist", "Medical Researcher", "Public Health Expert"],
        "salary_range": "$80,000 - $350,000",
        "job_growth": "13% (Faster than average)",
        "difficulty": 10,
        "dropout_rate": "15%",
        "work_life_balance": 4,
        "day_in_life": "🏥 6AM — Early rounds. Check on 8 patients before breakfast.\n📚 8AM — Lecture: Cardiovascular Pathology (take notes fast!).\n🔬 10AM — Lab: Analyze blood samples under a microscope.\n🍎 12PM — Quick lunch in the hospital cafeteria.\n👨‍⚕️ 1PM — Clinical rotation: Shadow a cardiologist during patient consultations.\n📖 6PM — Library: Study for tomorrow's anatomy exam.\n😴 10PM — Finally home. Set alarm for 5:30AM.",
        "reality_check": {
            "math_required": False,
            "message": "Medicine is a 7-10 year commitment (undergrad + residency). The workload is intense and burnout is real. But if you genuinely want to help people and can handle the pressure, it's one of the most rewarding careers. Ask yourself: Can I study 60+ hours/week for years?",
        },
        "roadmap": ["Year 1-2: Pre-clinical (Anatomy, Physiology)", "Year 3-4: Clinical rotations", "Year 5: Internship", "Year 6+: Residency & Specialization", "Job: Resident → Attending → Specialist"],
        "bridge_courses": ["Biology Refresher (Khan Academy)", "First Aid Basics", "Medical Terminology Course"],
    },
    "business_management": {
        "name": "Business / MBA Track",
        "emoji": "📊",
        "category": "Commerce",
        "required_tags": ["communication", "leadership", "math_basic", "people", "strategy"],
        "anti_tags": ["coding_heavy", "lab_work", "isolation"],
        "weights": {"math": 0.2, "communication": 0.4, "leadership": 0.4},
        "subjects": ["Marketing", "Finance", "Operations", "HR Management", "Entrepreneurship"],
        "careers": ["Business Analyst", "Marketing Manager", "Consultant", "Startup Founder", "Product Manager"],
        "salary_range": "$50,000 - $160,000",
        "job_growth": "12% (Faster than average)",
        "difficulty": 5,
        "dropout_rate": "10%",
        "work_life_balance": 7,
        "day_in_life": "☕ 9AM — Check market trends and emails. Prepare for a client pitch.\n📊 10AM — Analyze quarterly sales data in Excel + Tableau.\n🤝 11AM — Team brainstorm: new product launch strategy.\n🍽️ 12PM — Networking lunch with a potential partner.\n📈 2PM — Present the marketing plan to leadership. Nail it.\n💡 4PM — Work on your side startup idea: a subscription snack box.\n🏠 6PM — Wrap up. Read a chapter from \"Zero to One\".",
        "reality_check": {
            "math_required": False,
            "message": "Business is versatile but competitive. Grades alone won't get you ahead — it's about internships, networking, and real projects. If you're a people person who loves strategy, this is your arena.",
        },
        "roadmap": ["Year 1: Business Fundamentals", "Year 2: Specialization (Marketing/Finance)", "Year 3: Internships + Case Competitions", "Year 4: Industry Project + Placement", "Job: Analyst → Manager → Director"],
        "bridge_courses": ["Excel for Business (Coursera)", "Intro to Accounting", "Public Speaking (Toastmasters)"],
    },
    "data_science": {
        "name": "Data Science & Analytics",
        "emoji": "📈",
        "category": "STEM",
        "required_tags": ["math", "statistics", "logic", "curiosity", "technology"],
        "anti_tags": ["hate_math", "hate_sitting", "physical_labor"],
        "weights": {"math": 0.4, "statistics": 0.35, "logic": 0.25},
        "subjects": ["Statistics", "Machine Learning", "Python/R", "Data Visualization", "Big Data"],
        "careers": ["Data Analyst", "Data Scientist", "ML Engineer", "Business Intelligence", "Quantitative Analyst"],
        "salary_range": "$65,000 - $175,000",
        "job_growth": "36% (Much faster than average)",
        "difficulty": 7,
        "dropout_rate": "18%",
        "work_life_balance": 8,
        "day_in_life": "☕ 9AM — Jupyter Notebook open: clean a messy dataset from the sales team.\n📊 10AM — Build a dashboard in Tableau showing customer churn patterns.\n🤖 11AM — Train a machine learning model to predict next quarter's revenue.\n🍕 12PM — Lunch & learn: colleague demos a new NLP technique.\n📈 2PM — Present insights to the CEO: \"We're losing 12% of users in week 2.\"\n💡 4PM — Experiment with a new algorithm on Kaggle.\n🏠 6PM — Home. Scroll through r/datascience for fun.",
        "reality_check": {
            "math_required": True,
            "message": "Data Science is the 'sexiest job of the 21st century' — but 80% of the work is data cleaning, not AI wizardry. Strong math (linear algebra, statistics) is essential. If you enjoy finding patterns in chaos, this is your calling.",
        },
        "roadmap": ["Year 1: Math + Statistics + Python", "Year 2: ML & Data Engineering", "Year 3: Deep Learning & Specialization", "Year 4: Capstone + Internship", "Job: Analyst → Data Scientist → Lead"],
        "bridge_courses": ["Python for Beginners (freeCodeCamp)", "Statistics 101 (Khan Academy)", "SQL in 4 Hours (YouTube)"],
    },
    "design_arts": {
        "name": "Design & Creative Arts",
        "emoji": "🎨",
        "category": "Arts & Humanities",
        "required_tags": ["creativity", "visual_thinking", "empathy", "storytelling", "aesthetics"],
        "anti_tags": ["hate_subjectivity", "need_structure", "math_heavy"],
        "weights": {"creativity": 0.5, "empathy": 0.25, "tech_savvy": 0.25},
        "subjects": ["UI/UX Design", "Graphic Design", "Animation", "Film", "Typography"],
        "careers": ["UX Designer", "Graphic Designer", "Art Director", "Motion Designer", "Brand Strategist"],
        "salary_range": "$45,000 - $130,000",
        "job_growth": "16% (Faster than average)",
        "difficulty": 5,
        "dropout_rate": "12%",
        "work_life_balance": 8,
        "day_in_life": "🎨 9AM — Open Figma. Design a mobile app onboarding flow.\n☕ 10AM — User research call: interview 3 customers about their pain points.\n✏️ 11AM — Sketch wireframes on your iPad based on insights.\n🍽️ 12PM — Lunch + browse Dribbble for inspiration.\n🖥️ 2PM — High-fidelity mockups. Pick colors, fonts, micro-animations.\n🤝 4PM — Present designs to the product team. Iterate based on feedback.\n🏠 6PM — Work on your portfolio. Post a case study on Behance.",
        "reality_check": {
            "math_required": False,
            "message": "Design is not just 'making things pretty'. It's problem-solving with empathy. You'll need thick skin — your work gets critiqued constantly. But if you love making experiences better for people, the creative freedom is incredible.",
        },
        "roadmap": ["Year 1: Design Fundamentals & Tools", "Year 2: UX Research & Interaction Design", "Year 3: Portfolio Building + Internship", "Year 4: Specialization + Thesis", "Job: Junior Designer → Senior → Art Director"],
        "bridge_courses": ["Intro to Figma (YouTube)", "Design Thinking (IDEO)", "Color Theory Basics"],
    },
    "electrical_engineering": {
        "name": "Electrical & Electronics Eng.",
        "emoji": "⚡",
        "category": "Engineering",
        "required_tags": ["physics", "math", "circuits", "technology", "problem_solving"],
        "anti_tags": ["blood", "animals", "hate_math"],
        "weights": {"math": 0.4, "physics": 0.4, "logic": 0.2},
        "subjects": ["Circuit Theory", "Signal Processing", "Embedded Systems", "Power Systems", "VLSI"],
        "careers": ["Electrical Engineer", "Embedded Systems Developer", "Power Systems Engineer", "IoT Specialist"],
        "salary_range": "$65,000 - $150,000",
        "job_growth": "9% (Average)",
        "difficulty": 9,
        "dropout_rate": "22%",
        "work_life_balance": 6,
        "day_in_life": "⚡ 8AM — Lab session: wire up a circuit on a breadboard and test it with an oscilloscope.\n📐 10AM — Lecture: Electromagnetic Field Theory (tough but fascinating).\n💻 11AM — Code a microcontroller in C to control a robot arm.\n🍽️ 12PM — Lunch with lab partners.\n🔬 2PM — Simulation: model a power grid in MATLAB.\n📖 4PM — Study group: help each other with Laplace transforms.\n🏠 6PM — Home. Watch ElectroBOOM on YouTube for fun.",
        "reality_check": {
            "math_required": True,
            "message": "EEE is math-heavy and abstract (electromagnetic fields, Fourier transforms). But it's the backbone of everything — phones, cars, satellites, robots. If you love understanding how things work at a fundamental level, this is deeply satisfying.",
        },
        "roadmap": ["Year 1: Math + Physics foundations", "Year 2: Circuit Theory & Electronics", "Year 3: Specialization (Power/VLSI/Embedded)", "Year 4: Industry Project + Internship", "Job: Junior EE → Senior → Specialist"],
        "bridge_courses": ["Basic Electronics (YouTube)", "Arduino Starter Kit", "Physics Refresh (Khan Academy)"],
    },
    "biotechnology": {
        "name": "Biotechnology",
        "emoji": "🧬",
        "category": "Life Sciences",
        "required_tags": ["biology", "chemistry", "research", "curiosity", "lab_work"],
        "anti_tags": ["hate_lab", "hate_memorizing", "need_fast_results"],
        "weights": {"biology": 0.45, "chemistry": 0.35, "research": 0.2},
        "subjects": ["Genetics", "Biochemistry", "Bioinformatics", "Immunology", "Bioprocess Engineering"],
        "careers": ["Biotech Researcher", "Genetic Counselor", "Pharma Scientist", "Bioinformatics Analyst"],
        "salary_range": "$55,000 - $140,000",
        "job_growth": "11% (Faster than average)",
        "difficulty": 7,
        "dropout_rate": "17%",
        "work_life_balance": 7,
        "day_in_life": "🧪 8AM — Start a PCR experiment in the lab. Wear gloves and goggles.\n📚 10AM — Lecture: CRISPR gene editing and its ethical implications.\n🧬 11AM — Analyze DNA sequences on your computer using BLAST.\n🍽️ 12PM — Lunch + discuss a new cancer research paper.\n🔬 2PM — Lab: culture bacteria and observe under the microscope.\n📊 4PM — Write up results for your research paper.\n🏠 6PM — Home. Watch a documentary on genetic engineering.",
        "reality_check": {
            "math_required": False,
            "message": "Biotech is exciting (CRISPR! mRNA vaccines!) but research is slow — experiments can take weeks. Higher degrees (MS/PhD) are often needed for top roles. If you're patient and love biology, the impact you can make is enormous.",
        },
        "roadmap": ["Year 1: Biology + Chemistry foundations", "Year 2: Genetics & Biochemistry", "Year 3: Specialization + Lab Research", "Year 4: Thesis + Internship", "Job: Lab Researcher → Senior Scientist → R&D Lead"],
        "bridge_courses": ["Biology 101 (Khan Academy)", "Intro to Genetics (Coursera)", "Lab Safety Basics"],
    },
}

# ═══════════════════════════════════════════════════════════
# 2. PSYCHOMETRIC MINI-GAME — 5 questions
# ═══════════════════════════════════════════════════════════

PSYCHOMETRIC_QUESTIONS = [
    {
        "id": 1,
        "question": "On a Saturday afternoon, you'd rather…",
        "options": [
            {"label": "🔧 Build or fix something with your hands", "tags": ["hands_on", "building", "physical_labor"], "type": "Builder"},
            {"label": "📖 Read, research, or solve a puzzle", "tags": ["logic", "research", "curiosity"], "type": "Thinker"},
            {"label": "🗣️ Hang out, organize plans, or lead a group", "tags": ["communication", "leadership", "people"], "type": "Communicator"},
            {"label": "🎨 Draw, design, or create something new", "tags": ["creativity", "visual_thinking", "aesthetics"], "type": "Creator"},
        ],
    },
    {
        "id": 2,
        "question": "Which of these would stress you out the MOST?",
        "options": [
            {"label": "😰 Solving complex math equations all day", "anti_tags": ["math", "math_heavy"], "type": "anti"},
            {"label": "😰 Working alone in a lab for 8 hours", "anti_tags": ["lab_work", "isolation", "sitting_all_day"], "type": "anti"},
            {"label": "😰 Giving a presentation to 200 people", "anti_tags": ["communication", "leadership"], "type": "anti"},
            {"label": "😰 Seeing blood or doing dissections", "anti_tags": ["blood", "blood_phobia"], "type": "anti"},
        ],
    },
    {
        "id": 3,
        "question": "What kind of problems do you want to solve?",
        "options": [
            {"label": "🌍 Climate, energy, sustainability", "tags": ["physics", "building", "outdoors"], "type": "mission"},
            {"label": "🏥 Health, diseases, saving lives", "tags": ["biology", "chemistry", "empathy", "helping_people"], "type": "mission"},
            {"label": "💻 Making technology smarter & faster", "tags": ["logic", "technology", "math", "problem_solving"], "type": "mission"},
            {"label": "💰 Business, money, entrepreneurship", "tags": ["communication", "strategy", "leadership", "math_basic"], "type": "mission"},
        ],
    },
    {
        "id": 4,
        "question": "Your ideal work environment looks like…",
        "options": [
            {"label": "🏢 Office with a team & meetings", "tags": ["people", "communication", "leadership"], "type": "environment"},
            {"label": "💻 Remote, headphones on, deep focus", "tags": ["sitting", "logic", "technology", "sitting_all_day"], "type": "environment"},
            {"label": "🔬 A lab with equipment & experiments", "tags": ["lab_work", "research", "hands_on"], "type": "environment"},
            {"label": "🌳 Outdoors, moving around, fieldwork", "tags": ["outdoors", "physical_labor", "hands_on"], "type": "environment"},
        ],
    },
    {
        "id": 5,
        "question": "What matters MOST to you in a career?",
        "options": [
            {"label": "💰 High salary & financial security", "tags": ["math", "technology", "strategy"], "priority": "salary"},
            {"label": "❤️ Making a real difference in people's lives", "tags": ["empathy", "helping_people", "biology"], "priority": "impact"},
            {"label": "🎨 Creative freedom & self-expression", "tags": ["creativity", "visual_thinking", "storytelling"], "priority": "creativity"},
            {"label": "⚖️ Work-life balance & stability", "tags": ["math_basic", "communication"], "priority": "balance"},
        ],
    },
]

# ═══════════════════════════════════════════════════════════
# 3. ANTI-CHOICE FILTER QUESTIONS
# ═══════════════════════════════════════════════════════════

ANTI_CHOICE_QUESTIONS = [
    {"id": "ac1", "question": "Do you hate looking at blood or doing dissections?", "anti_tags": ["blood", "blood_phobia"]},
    {"id": "ac2", "question": "Do you hate sitting at a computer for hours?", "anti_tags": ["sitting", "sitting_all_day", "coding_heavy"]},
    {"id": "ac3", "question": "Do you hate memorizing lots of facts and definitions?", "anti_tags": ["hate_memorizing"]},
    {"id": "ac4", "question": "Do you hate doing math and equations?", "anti_tags": ["math", "math_heavy", "hate_math"]},
    {"id": "ac5", "question": "Do you hate working alone for long stretches?", "anti_tags": ["isolation", "research", "lab_work"]},
    {"id": "ac6", "question": "Do you hate speaking in front of people?", "anti_tags": ["communication", "leadership"]},
]

# ═══════════════════════════════════════════════════════════
# 4. REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════

class OriginStoryInput(BaseModel):
    # Anti-choice: list of anti_tag IDs the user said YES to
    anti_choices: List[str] = []  # e.g. ["ac1", "ac4"]
    # Psychometric answers: question_id -> selected option index (0-3)
    psychometric_answers: Dict[str, int] = {}
    # Academic strengths (self-reported or parsed)
    strong_subjects: List[str] = []  # e.g. ["math", "physics", "biology"]
    # Interest tags
    interests: List[str] = []  # e.g. ["#Robots", "#AI", "#Money"]
    # Constraints
    budget: Optional[str] = "flexible"  # low, medium, high, flexible
    location_pref: Optional[str] = ""


class StreamRecommendation(BaseModel):
    rank: int
    stream_id: str
    name: str
    emoji: str
    match_score: int  # 0-100
    pitch: str
    salary_range: str
    job_growth: str
    difficulty: int
    work_life_balance: int
    day_in_life: str
    reality_check: str
    roadmap: List[str]
    bridge_courses: List[str]
    careers: List[str]
    subjects: List[str]


# ═══════════════════════════════════════════════════════════
# 5. MATCHING ENGINE
# ═══════════════════════════════════════════════════════════

def _compute_match(user_tags: List[str], user_anti_tags: List[str], stream: Dict) -> int:
    """Compute a 0-100 match score using weighted tag overlap."""
    # Hard exclusion: if user anti-tags intersect stream required tags
    anti_overlap = set(user_anti_tags) & set(stream.get("required_tags", []))
    if len(anti_overlap) >= 2:
        return 0  # strong disqualification

    # Positive match: overlap between user tags and stream required tags
    required = set(stream.get("required_tags", []))
    positive_overlap = set(user_tags) & required
    if not required:
        return 50

    base_score = (len(positive_overlap) / len(required)) * 80

    # Penalty for partial anti-tag overlap
    penalty = len(anti_overlap) * 15

    # Bonus for strong interest alignment
    bonus = min(len(positive_overlap), 3) * 5

    return max(0, min(100, int(base_score - penalty + bonus)))


def _generate_pitch(stream: Dict, user_interests: List[str]) -> str:
    """Generate a personalized 'Why this fits you' pitch."""
    name = stream["name"]
    careers_str = ", ".join(stream["careers"][:3])
    interests_str = ", ".join(user_interests[:3]) if user_interests else "your passions"

    pitches = {
        "computer_science": f"You love logic, problem-solving, and tech — {name} turns that into a superpower. With careers like {careers_str}, you'll build the tools millions use daily. Your interest in {interests_str} aligns perfectly with the tech world.",
        "mechanical_engineering": f"You're a builder at heart. {name} lets you design, prototype, and create real things — from drones to electric cars. Careers like {careers_str} await. Your hands-on nature is your biggest asset.",
        "medicine": f"Your empathy and love for biology make you a natural healer. {name} is tough but incredibly rewarding — you'll literally save lives. Careers like {careers_str} are among the most respected globally.",
        "business_management": f"You're a people person with strategic instincts. {name} channels your communication and leadership skills into high-impact roles like {careers_str}. Your interest in {interests_str} shows entrepreneurial potential.",
        "data_science": f"You see patterns where others see chaos. {name} combines math, coding, and curiosity into one of the fastest-growing fields. Careers like {careers_str} are in massive demand.",
        "design_arts": f"Your creativity isn't just a hobby — it's a career advantage. {name} turns your visual sense and empathy into experiences used by millions. Roles like {careers_str} offer creative freedom and impact.",
        "electrical_engineering": f"You're fascinated by how things work at a fundamental level. {name} is the backbone of modern civilization — power grids, robots, phones all depend on it. Careers like {careers_str} are always in demand.",
        "biotechnology": f"You're curious about life at a molecular level. {name} is at the frontier of CRISPR, mRNA, and personalized medicine. Careers like {careers_str} let you shape the future of healthcare.",
    }
    return pitches.get(stream.get("_id", ""), f"Based on your profile, {name} is a strong match! With careers like {careers_str} and your interest in {interests_str}, this path offers both growth and fulfilment.")


def recommend_streams(input_data: OriginStoryInput) -> List[Dict]:
    """Run the full matching engine and return ranked recommendations."""

    # 1. Collect user anti-tags from anti-choice questions
    user_anti_tags = []
    for ac_id in input_data.anti_choices:
        aq = next((q for q in ANTI_CHOICE_QUESTIONS if q["id"] == ac_id), None)
        if aq:
            user_anti_tags.extend(aq["anti_tags"])

    # 2. Collect user positive tags from psychometric answers
    user_tags = []
    archetype_counts = {"Builder": 0, "Thinker": 0, "Communicator": 0, "Creator": 0}
    for q_id_str, option_idx in input_data.psychometric_answers.items():
        q_id = int(q_id_str) if q_id_str.isdigit() else 0
        question = next((q for q in PSYCHOMETRIC_QUESTIONS if q["id"] == q_id), None)
        if question and 0 <= option_idx < len(question["options"]):
            option = question["options"][option_idx]
            user_tags.extend(option.get("tags", []))
            # Track anti-tags from psychometric stress question
            if option.get("type") == "anti":
                user_anti_tags.extend(option.get("anti_tags", []))
            # Track archetype
            archetype = option.get("type", "")
            if archetype in archetype_counts:
                archetype_counts[archetype] += 1

    # 3. Add academic strengths as tags
    subject_tag_map = {
        "math": ["math", "logic", "statistics"],
        "physics": ["physics", "building", "problem_solving"],
        "chemistry": ["chemistry", "lab_work"],
        "biology": ["biology", "research"],
        "english": ["communication", "storytelling"],
        "computer": ["technology", "logic", "coding_heavy"],
        "art": ["creativity", "visual_thinking", "aesthetics"],
        "economics": ["strategy", "math_basic"],
    }
    for subj in input_data.strong_subjects:
        user_tags.extend(subject_tag_map.get(subj.lower(), [subj.lower()]))

    # 4. Add interest tags
    interest_tag_map = {
        "robots": ["technology", "building", "hands_on"],
        "ai": ["logic", "math", "technology"],
        "money": ["strategy", "math_basic", "leadership"],
        "writing": ["communication", "storytelling", "creativity"],
        "gaming": ["technology", "logic", "creativity"],
        "outdoors": ["outdoors", "physical_labor", "hands_on"],
        "music": ["creativity", "aesthetics"],
        "science": ["research", "curiosity", "lab_work"],
        "sports": ["hands_on", "outdoors", "leadership"],
        "helping": ["empathy", "helping_people"],
    }
    for interest in input_data.interests:
        clean = interest.lower().strip("#").strip()
        user_tags.extend(interest_tag_map.get(clean, [clean]))

    # 5. Deduplicate
    user_tags = list(set(user_tags))
    user_anti_tags = list(set(user_anti_tags))

    # 6. Score each stream
    scored = []
    for stream_id, stream in STREAMS.items():
        stream_with_id = {**stream, "_id": stream_id}
        score = _compute_match(user_tags, user_anti_tags, stream)
        if score > 0:
            scored.append((stream_id, stream, score))

    # 7. Sort by score descending, take top 3
    scored.sort(key=lambda x: x[2], reverse=True)
    top = scored[:3]

    # 8. Build results
    results = []
    for rank, (stream_id, stream, score) in enumerate(top, 1):
        stream_with_id = {**stream, "_id": stream_id}
        results.append({
            "rank": rank,
            "stream_id": stream_id,
            "name": stream["name"],
            "emoji": stream["emoji"],
            "match_score": score,
            "pitch": _generate_pitch(stream_with_id, input_data.interests),
            "salary_range": stream["salary_range"],
            "job_growth": stream["job_growth"],
            "difficulty": stream["difficulty"],
            "work_life_balance": stream["work_life_balance"],
            "day_in_life": stream["day_in_life"],
            "reality_check": stream["reality_check"]["message"],
            "roadmap": stream["roadmap"],
            "bridge_courses": stream["bridge_courses"],
            "careers": stream["careers"],
            "subjects": stream["subjects"],
        })

    # If fewer than 3 results, pad with fallbacks
    if len(results) < 3:
        for stream_id, stream in STREAMS.items():
            if stream_id not in [r["stream_id"] for r in results]:
                stream_with_id = {**stream, "_id": stream_id}
                results.append({
                    "rank": len(results) + 1,
                    "stream_id": stream_id,
                    "name": stream["name"],
                    "emoji": stream["emoji"],
                    "match_score": 40,
                    "pitch": _generate_pitch(stream_with_id, input_data.interests),
                    "salary_range": stream["salary_range"],
                    "job_growth": stream["job_growth"],
                    "difficulty": stream["difficulty"],
                    "work_life_balance": stream["work_life_balance"],
                    "day_in_life": stream["day_in_life"],
                    "reality_check": stream["reality_check"]["message"],
                    "roadmap": stream["roadmap"],
                    "bridge_courses": stream["bridge_courses"],
                    "careers": stream["careers"],
                    "subjects": stream["subjects"],
                })
                if len(results) >= 3:
                    break

    return results


# ═══════════════════════════════════════════════════════════
# 6. ENDPOINTS
# ═══════════════════════════════════════════════════════════

@router.get("/questions")
def get_origin_story_questions():
    """Get all onboarding questions for the Origin Story flow."""
    return {
        "psychometric_questions": PSYCHOMETRIC_QUESTIONS,
        "anti_choice_questions": ANTI_CHOICE_QUESTIONS,
        "interest_options": [
            "#Robots", "#AI", "#Money", "#Writing", "#Gaming",
            "#Outdoors", "#Music", "#Science", "#Sports", "#Helping",
            "#Art", "#Coding", "#Business", "#Health", "#Space",
        ],
        "subject_options": [
            "Math", "Physics", "Chemistry", "Biology",
            "English", "Computer", "Art", "Economics",
        ],
    }


@router.post("/recommend")
def get_stream_recommendations(
    input_data: OriginStoryInput,
    current_user: User = Depends(get_current_user),
):
    """Run the matching engine and return top 3 stream recommendations."""
    results = recommend_streams(input_data)
    return {"recommendations": results, "total_streams_analyzed": len(STREAMS)}


@router.get("/stream/{stream_id}")
def get_stream_detail(stream_id: str):
    """Get detailed info about a specific stream."""
    stream = STREAMS.get(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {**stream, "stream_id": stream_id}
