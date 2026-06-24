from app.resume.analyzer import (
    ResumeAnalyzer
)

analyzer = (
    ResumeAnalyzer()
)

resume_text = """

Python
FastAPI
SQL
Docker

Built AI Interview Analytics
Built SkillTwin AI

"""

result = (
    analyzer.analyze(
        resume_text
    )
)

print()

print(
    "EXTRACTED SKILLS:"
)

print(
    result.extracted_skills
)

print()

print(
    "MISSING SKILLS:"
)

print(
    result.missing_skills
)

print()

print(
    "PROJECTS:"
)

print(
    result.recommended_projects
)

print()

print(
    "READINESS SCORE:"
)

print(
    result.readiness_score
)