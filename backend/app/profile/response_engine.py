from app.profile.models import (
    UserProfile
)


class PersonalizedResponseEngine:

    def generate(
        self,
        profile: UserProfile
    ):

        response = []

        response.append(
            f"Current Goal: "
            f"{profile.primary_goal}"
        )

        response.append("")

        response.append(
            "Known Skills:"
        )

        for skill in profile.skills:

            response.append(
                f"- {skill}"
            )

        response.append("")

        response.append(
            "Missing Skills:"
        )

        for skill in profile.missing_skills:

            response.append(
                f"- {skill}"
            )

        response.append("")

        response.append(
            "Projects:"
        )

        for project in profile.projects:

            response.append(
                f"- {project}"
            )

        response.append("")

        response.append(
            f"Reflection Score: "
            f"{profile.reflection_score}/10"
        )

        response.append("")

        # Recommendation Logic

        if profile.missing_skills:

            next_skill = (
                profile.missing_skills[0]
            )

            response.append(
                f"Recommended Next Step: "
                f"{next_skill}"
            )

        else:

            response.append(
                "Recommended Next Step: "
                "Build advanced projects."
            )

        return "\n".join(
            response
        )