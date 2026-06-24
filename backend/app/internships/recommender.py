class InternshipRecommender:

    def recommend(
        self,
        skills
    ):

        recommendations = []

        if "Python" in skills:

            recommendations.append(
                "Python Developer Intern"
            )

        if "Machine Learning" in skills:

            recommendations.append(
                "Machine Learning Intern"
            )

        if "Data Analysis" in skills:

            recommendations.append(
                "Data Analyst Intern"
            )

        if "SQL" in skills:

            recommendations.append(
                "Database Intern"
            )

        if "HTML" in skills and "JavaScript" in skills:

            recommendations.append(
                "Frontend Developer Intern"
            )

        return recommendations