from app.profile.models import (
    UserProfile
)

profile = UserProfile(

    user_id="user123",

    primary_goal="AI Internship",

    skills=[
        "Python",
        "FastAPI"
    ],

    missing_skills=[
        "Git",
        "GitHub"
    ],

    projects=[
        "SkillTwin AI"
    ],

    reflection_score=8
)

print(profile)