import streamlit as st

from services.api import (
    upload_resume
)

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

# ======================
# HEADER
# ======================

header_col1, header_col2 = st.columns(
    [1, 4]
)

with header_col1:

    st.image(
        "assets/logo.png",
        width=120
    )

with header_col2:

    st.title(
        "📄 Resume Intelligence"
    )

    st.caption(
        "Analyze resumes, identify skill gaps, recommend projects and internships."
    )

st.divider()

# ======================
# UPLOAD
# ======================

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "Analyze Resume",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing Resume..."
        ):

            result = upload_resume(
                uploaded_file
            )

        score = result[
            "readiness_score"
        ]

        percentage = score * 10

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

        # ======================
        # METRICS
        # ======================

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "🧠 Skills",
                skills_count
            )

        with m2:

            st.metric(
                "⚠ Missing",
                missing_count
            )

        with m3:

            st.metric(
                "🚀 Projects",
                project_count
            )

        with m4:

            st.metric(
                "📊 Readiness",
                f"{percentage}%"
            )

        st.divider()

        # ======================
        # CAREER REPORT
        # ======================

        st.subheader(
            "📊 Career Report"
        )

        report1, report2 = st.columns(2)

        with report1:

            st.metric(
                "Readiness Score",
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

        # ======================
        # SKILLS
        # ======================

        left, right = st.columns(2)

        with left:

            st.subheader(
                "✅ Extracted Skills"
            )

            st.write(
                ", ".join(
                    result[
                        "extracted_skills"
                    ]
                )
            )

        with right:

            st.subheader(
                "⚠ Missing Skills"
            )

            st.write(
                ", ".join(
                    result[
                        "missing_skills"
                    ]
                )
            )

        st.divider()

        # ======================
        # PROJECTS + INTERNSHIPS
        # ======================

        left, right = st.columns(2)

        with left:

            st.subheader(
                "🚀 Recommended Projects"
            )

            for project in result[
                "recommended_projects"
            ]:

                st.info(
                    project
                )

        with right:

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

        st.caption(
            f"""
            Skills Found: {skills_count} |
            Missing Skills: {missing_count} |
            Projects Suggested: {project_count} |
            Internships Suggested: {internship_count}
            """
        )

st.divider()

st.caption(
    "SkillTwin AI v1.0 • Resume Intelligence Engine"
)