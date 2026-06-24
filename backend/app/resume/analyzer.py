from app.resume.models import (
    ResumeAnalysis
)

from app.resume.extractor import (
    SkillExtractor
)


class ResumeAnalyzer:

    def __init__(self):

        self.extractor = (
            SkillExtractor()
        )

    def analyze(
        self,
        resume_text: str
    ):

        analysis = (
            ResumeAnalysis()
        )

        skills = (
            self.extractor.extract(
                resume_text
            )
        )

        analysis.extracted_skills = (
            skills
        )

        target_skills = [

            "Python",
            "Git",
            "GitHub",
            "FastAPI",
            "Docker"
        ]

        for skill in target_skills:

            if skill not in skills:

                analysis.missing_skills.append(
                    skill
                )

        analysis.recommended_projects = [

            "AI Interview Analytics",

            "Resume Intelligence",

            "SkillTwin AI"
        ]

        analysis.readiness_score = (

            max(
                0,
                10 - len(
                    analysis.missing_skills
                )
            )
        )

        return analysis