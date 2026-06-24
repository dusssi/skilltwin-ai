class SkillExtractor:

    def extract(
        self,
        text: str
    ):

        skills = []

        text = text.lower()

        known_skills = [

            "Python",
            "Java",
            "C",
            "C++",
            "SQL",

            "Git",
            "GitHub",

            "FastAPI",
            "Flask",
            "Django",

            "Docker",
            "Kubernetes",

            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Computer Vision",

            "TensorFlow",
            "PyTorch",
            "Scikit-Learn",

            "Data Analysis",
            "Data Visualization",

            "MongoDB",
            "PostgreSQL",
            "MySQL",

            "HTML",
            "CSS",
            "JavaScript",

            "React",
            "Node.js",

            "Android Studio",

            "Recommendation Systems",

            "Operating Systems",
            "DBMS",
            "OOP",

            "Linux",
            "AWS"
        ]

        for skill in known_skills:

            if skill.lower() in text:

                skills.append(
                    skill
                )

        return skills