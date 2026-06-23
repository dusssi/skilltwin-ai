from app.profile.models import (
    UserProfile
)

from app.profile.profile_updater import (
    ProfileUpdater
)

profile = UserProfile(
    user_id="user123",
    primary_goal="AI Internship"
)

updater = ProfileUpdater()

updated_profile = (
    updater.update_profile(

        profile=profile,

        skills=[
            "Python",
            "FastAPI",
            "SQL"
        ],

        projects=[
            "SkillTwin AI"
        ],

        reflection={

            "issues": [
                "Git missing",
                "GitHub missing"
            ],

            "score": 8
        }
    )
)

print(updated_profile)