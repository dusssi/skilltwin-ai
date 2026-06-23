from app.reflection.models import (
    ReflectionResult
)


class Reflector:

    def reflect(
        self,
        skills: list
    ):

        result = ReflectionResult()

        expected_skills = [

            "Python",
            "Git",
            "GitHub",
            "Docker"
        ]

        for skill in expected_skills:

            if skill not in skills:

                result.issues.append(
                    f"{skill} missing"
                )

                result.suggestions.append(
                    f"Learn {skill}"
                )

        result.score = (
            10 - len(result.issues)
        )

        if result.score < 0:

            result.score = 0

        return result