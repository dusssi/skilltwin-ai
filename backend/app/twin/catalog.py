"""Canonical skill catalog: names, aliases and categories.

The resume extractor and the Twin merge logic share this catalog so skill
identity is consistent everywhere. Aliases let e.g. ``scikit-learn``,
``sklearn`` and ``Scikit-Learn`` resolve to one skill.
"""

SKILL_CATALOG: list = [
    {"name": "Python", "aliases": ["python3", "py"], "category": "language"},
    {"name": "Java", "aliases": [], "category": "language"},
    {"name": "C", "aliases": [], "category": "language"},
    {"name": "C++", "aliases": ["cpp", "c plus plus"], "category": "language"},
    {"name": "C#", "aliases": ["c sharp", "csharp"], "category": "language"},
    {"name": "JavaScript", "aliases": ["js", "ecmascript"], "category": "language"},
    {"name": "TypeScript", "aliases": ["ts"], "category": "language"},
    {"name": "Go", "aliases": ["golang"], "category": "language"},
    {"name": "SQL", "aliases": ["structured query language"], "category": "data"},
    {"name": "HTML", "aliases": ["html5"], "category": "frontend"},
    {"name": "CSS", "aliases": ["css3"], "category": "frontend"},
    {"name": "React", "aliases": ["reactjs", "react.js"], "category": "frontend"},
    {"name": "Node.js", "aliases": ["nodejs", "node"], "category": "backend"},
    {"name": "FastAPI", "aliases": ["fast api"], "category": "backend"},
    {"name": "Flask", "aliases": [], "category": "backend"},
    {"name": "Django", "aliases": [], "category": "backend"},
    {"name": "PostgreSQL", "aliases": ["postgres", "psql"], "category": "backend"},
    {"name": "MySQL", "aliases": [], "category": "backend"},
    {"name": "MongoDB", "aliases": ["mongo"], "category": "backend"},
    {"name": "Redis", "aliases": [], "category": "backend"},
    {"name": "Git", "aliases": [], "category": "tooling"},
    {"name": "GitHub", "aliases": ["github actions"], "category": "tooling"},
    {"name": "Docker", "aliases": ["dockerfile", "docker compose", "containerization"],
     "category": "devops"},
    {"name": "Kubernetes", "aliases": ["k8s"], "category": "devops"},
    {"name": "Linux", "aliases": ["ubuntu", "bash", "shell scripting"], "category": "devops"},
    {"name": "AWS", "aliases": ["amazon web services", "ec2", "s3"], "category": "devops"},
    {"name": "Machine Learning", "aliases": ["ml"], "category": "ai"},
    {"name": "Deep Learning", "aliases": ["dl", "neural networks"], "category": "ai"},
    {"name": "NLP", "aliases": ["natural language processing"], "category": "ai"},
    {"name": "Computer Vision", "aliases": ["cv", "image processing"], "category": "ai"},
    {"name": "TensorFlow", "aliases": ["tf"], "category": "ai"},
    {"name": "PyTorch", "aliases": ["torch"], "category": "ai"},
    {"name": "Scikit-Learn", "aliases": ["sklearn", "scikit learn"], "category": "ai"},
    {"name": "Pandas", "aliases": [], "category": "data"},
    {"name": "NumPy", "aliases": ["numpy"], "category": "data"},
    {"name": "Data Analysis", "aliases": ["data analytics", "eda"], "category": "data"},
    {"name": "Data Visualization", "aliases": ["data viz", "matplotlib", "tableau",
                                               "power bi", "powerbi"], "category": "data"},
    {"name": "Statistics", "aliases": ["statistical analysis"], "category": "data"},
    {"name": "Mathematics", "aliases": ["linear algebra", "calculus"], "category": "cs"},
    {"name": "Excel", "aliases": ["ms excel", "spreadsheets"], "category": "data"},
    {"name": "DSA", "aliases": ["data structures", "algorithms",
                                "data structures and algorithms"], "category": "cs"},
    {"name": "Operating Systems", "aliases": ["os fundamentals"], "category": "cs"},
    {"name": "DBMS", "aliases": ["database management systems"], "category": "cs"},
    {"name": "OOP", "aliases": ["object oriented programming",
                                "object-oriented programming"], "category": "cs"},
    {"name": "System Design", "aliases": ["distributed systems"], "category": "cs"},
    {"name": "Testing", "aliases": ["pytest", "unit testing", "qa"], "category": "tooling"},
    {"name": "Recommendation Systems", "aliases": ["recommender systems"], "category": "ai"},
    {"name": "Android", "aliases": ["android studio", "kotlin"], "category": "mobile"},
    {"name": "Communication", "aliases": ["technical writing", "documentation"], "category": "soft"},
    {"name": "Problem Solving", "aliases": ["analytical thinking"], "category": "soft"},
]


def seed_catalog() -> int:
    """Insert catalog skills into the DB skill table. Returns count ensured."""
    from app.db import twin as twin_repo

    count = 0
    for entry in SKILL_CATALOG:
        twin_repo.ensure_skill(
            entry["name"], aliases=entry.get("aliases", []),
            category=entry.get("category", ""),
        )
        count += 1
    return count
