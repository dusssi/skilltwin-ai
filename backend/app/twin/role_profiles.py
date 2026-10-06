"""Target-role skill rubrics used by the skill-gap engine.

Each role maps required skills to a target proficiency level (1-5) and an
importance weight (1-5). These rubrics are transparent, versioned data — not
hidden magic — and can be extended or replaced without touching the engine.
"""

ROLE_PROFILES: dict = {
    "ai_intern": {
        "label": "AI Intern",
        "match_keywords": ["ai intern", "ai internship", "artificial intelligence intern"],
        "skills": {
            "Python": {"target": 4, "importance": 5},
            "Git": {"target": 3, "importance": 4},
            "GitHub": {"target": 3, "importance": 4},
            "Machine Learning": {"target": 3, "importance": 5},
            "SQL": {"target": 3, "importance": 4},
            "FastAPI": {"target": 3, "importance": 3},
            "Docker": {"target": 2, "importance": 3},
            "Data Analysis": {"target": 3, "importance": 4},
            "Mathematics": {"target": 3, "importance": 3},
            "Communication": {"target": 3, "importance": 3},
        },
    },
    "ml_engineer": {
        "label": "Machine Learning Engineer",
        "match_keywords": ["ml engineer", "machine learning engineer", "ml "],
        "skills": {
            "Python": {"target": 5, "importance": 5},
            "Machine Learning": {"target": 4, "importance": 5},
            "Deep Learning": {"target": 4, "importance": 5},
            "PyTorch": {"target": 4, "importance": 4},
            "TensorFlow": {"target": 3, "importance": 3},
            "SQL": {"target": 4, "importance": 4},
            "Docker": {"target": 4, "importance": 4},
            "Git": {"target": 4, "importance": 4},
            "Linux": {"target": 3, "importance": 3},
            "Mathematics": {"target": 4, "importance": 4},
        },
    },
    "data_analyst": {
        "label": "Data Analyst",
        "match_keywords": ["data analyst", "data analytics", "analytics"],
        "skills": {
            "Python": {"target": 4, "importance": 4},
            "SQL": {"target": 4, "importance": 5},
            "Data Analysis": {"target": 4, "importance": 5},
            "Data Visualization": {"target": 4, "importance": 5},
            "Pandas": {"target": 4, "importance": 4},
            "Statistics": {"target": 4, "importance": 4},
            "Excel": {"target": 3, "importance": 3},
            "Communication": {"target": 4, "importance": 4},
            "Git": {"target": 2, "importance": 2},
        },
    },
    "backend_developer": {
        "label": "Backend Developer",
        "match_keywords": ["backend", "back-end", "server developer", "api developer"],
        "skills": {
            "Python": {"target": 4, "importance": 5},
            "FastAPI": {"target": 4, "importance": 5},
            "SQL": {"target": 4, "importance": 5},
            "PostgreSQL": {"target": 3, "importance": 4},
            "Git": {"target": 4, "importance": 4},
            "GitHub": {"target": 4, "importance": 3},
            "Docker": {"target": 3, "importance": 4},
            "Linux": {"target": 3, "importance": 3},
            "System Design": {"target": 3, "importance": 3},
            "Testing": {"target": 3, "importance": 3},
        },
    },
    "frontend_developer": {
        "label": "Frontend Developer",
        "match_keywords": ["frontend", "front-end", "react", "web developer"],
        "skills": {
            "HTML": {"target": 4, "importance": 5},
            "CSS": {"target": 4, "importance": 5},
            "JavaScript": {"target": 4, "importance": 5},
            "React": {"target": 4, "importance": 4},
            "Git": {"target": 3, "importance": 4},
            "GitHub": {"target": 3, "importance": 3},
            "Testing": {"target": 3, "importance": 3},
            "Communication": {"target": 3, "importance": 3},
        },
    },
    "general": {
        "label": "General Software Career",
        "match_keywords": [],
        "skills": {
            "Python": {"target": 3, "importance": 4},
            "Git": {"target": 3, "importance": 4},
            "GitHub": {"target": 3, "importance": 3},
            "SQL": {"target": 3, "importance": 3},
            "Communication": {"target": 3, "importance": 4},
            "Problem Solving": {"target": 4, "importance": 4},
        },
    },
}


def match_role(target_role: str) -> str:
    """Map free-text target role to the closest rubric key."""
    text = (target_role or "").strip().lower()
    if not text:
        return "general"
    for key, profile in ROLE_PROFILES.items():
        if key == "general":
            continue
        if profile["label"].lower() in text or text in profile["label"].lower():
            return key
        for keyword in profile["match_keywords"]:
            if keyword.strip() and keyword.strip() in text:
                return key
    return "general"


def get_role_profile(role_key: str) -> dict:
    return ROLE_PROFILES.get(role_key, ROLE_PROFILES["general"])
