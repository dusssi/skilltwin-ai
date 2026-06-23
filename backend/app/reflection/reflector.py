from app.reflection.models import (
    ReflectionResult
)


class Reflector:

    def reflect(
        self,
        profile: dict,
        completed_tasks: list,
        action_results: dict
    ):

        result = ReflectionResult()

        missing_skills = (

            profile.get(
                "missing_skills",
                []
            )
        )

        resolved_skills = []

        for task in completed_tasks:

            task = task.lower()

            if "git" in task:

                resolved_skills.append(
                    "Git missing"
                )

            if "github" in task:

                resolved_skills.append(
                    "GitHub missing"
                )

            if "docker" in task:

                resolved_skills.append(
                    "Docker missing"
                )

            if "python" in task:

                resolved_skills.append(
                    "Python missing"
                )

        remaining_skills = []

        for skill in missing_skills:

            if skill not in resolved_skills:

                remaining_skills.append(
                    skill
                )

        result.issues = (
            remaining_skills
        )

        for skill in remaining_skills:

            clean_skill = (
                skill.replace(
                    " missing",
                    ""
                )
            )

            result.suggestions.append(
                f"Learn {clean_skill}"
            )

        total_missing = (
            len(missing_skills)
        )

        remaining = (
            len(remaining_skills)
        )

        if total_missing == 0:

            result.score = 10

        else:

            progress = (
                total_missing -
                remaining
            )

            result.score = int(

                5 +

                (
                    progress /
                    total_missing
                ) * 5
            )

        return result