class SkillExtractor:

    def extract(
        self,
        text: str
    ):

        skills = []

        known_skills = [

            "Python",
            "FastAPI",
            "Docker",
            "SQL",
            "Git",
            "GitHub",
            "Machine Learning",
            "Deep Learning"
        ]

        for skill in known_skills:

            if skill.lower() in text.lower():

                skills.append(
                    skill
                )

        return skills