import streamlit as st

from services.api import (
    upload_resume
)

st.set_page_config(

    page_title="Resume Intelligence",

    page_icon="📄",

    layout="wide"
)

st.title(
    "📄 Resume Intelligence"
)

uploaded_file = st.file_uploader(

    "Upload Resume PDF",

    type=["pdf"]
)

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "Analyze Resume"
    ):

        with st.spinner(
            "Analyzing Resume..."
        ):

            result = (
                upload_resume(
                    uploaded_file
                )
            )

        score = result[
            "readiness_score"
        ]

        percentage = (
            score * 10
        )

        skills_count = len(
            result[
                "extracted_skills"
            ]
        )

        missing_count = len(
            result[
                "missing_skills"
            ]
        )

        project_count = len(
            result[
                "recommended_projects"
            ]
        )

        internship_count = len(
            result[
                "recommended_internships"
            ]
        )

        st.divider()

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            st.metric(
                "🧠 Skills",
                skills_count
            )

        with metric2:

            st.metric(
                "⚠️ Missing",
                missing_count
            )

        with metric3:

            st.metric(
                "🚀 Projects",
                project_count
            )

        with metric4:

            st.metric(
                "📊 Readiness",
                f"{percentage}%"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "✅ Extracted Skills"
            )

            for skill in result[
                "extracted_skills"
            ]:

                st.success(
                    skill
                )

        with col2:

            st.subheader(
                "⚠️ Missing Skills"
            )

            for skill in result[
                "missing_skills"
            ]:

                st.warning(
                    skill
                )

        st.divider()

        col3, col4 = st.columns(2)

        with col3:

            st.subheader(
                "🚀 Recommended Projects"
            )

            for project in result[
                "recommended_projects"
            ]:

                st.info(
                    project
                )

        with col4:

            st.subheader(
                "🎯 Recommended Internships"
            )

            for internship in result[
                "recommended_internships"
            ]:

                st.success(
                    internship
                )

        st.divider()

        st.subheader(
            "📊 Career Report"
        )

        report1, report2 = st.columns(2)

        with report1:

            st.metric(

                "Career Readiness Score",

                f"{score}/10"
            )

        with report2:

            st.metric(

                "Readiness Level",

                f"{percentage}%"
            )

        st.progress(
            score / 10
        )

        if score >= 9:

            st.success(
                "🚀 Excellent Internship Readiness"
            )

        elif score >= 7:

            st.info(
                "👍 Good Internship Readiness"
            )

        else:

            st.warning(
                "📚 Needs Improvement"
            )

        st.divider()

        st.caption(
            f"""
            Skills Found: {skills_count} |
            Missing Skills: {missing_count} |
            Projects Suggested: {project_count} |
            Internships Suggested: {internship_count}
            """
        )