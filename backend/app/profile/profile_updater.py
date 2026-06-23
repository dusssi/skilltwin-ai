from app.profile.models import (
    UserProfile
)


class ProfileUpdater:

    def update_profile(
        self,
        profile: UserProfile,
        skills: list,
        projects: list,
        reflection: dict
    ):

        profile.skills = skills

        profile.projects = projects

        profile.missing_skills = (

            reflection.get(
                "issues",
                []
            )
        )

        profile.reflection_score = (

            reflection.get(
                "score",
                0
            )
        )

        return profile