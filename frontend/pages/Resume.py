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

        st.subheader(
            "🚀 Recommended Projects"
        )

        for project in result[
            "recommended_projects"
        ]:

            st.info(
                project
            )

        st.divider()

        score = result[
            "readiness_score"
        ]

        st.subheader(
            "📊 Career Report"
        )

        st.metric(

            "Career Readiness Score",

            f"{score}/10"
        )

        st.progress(
            score / 10
        )
        percentage = score * 10

        st.caption(
            f"Readiness Level: {percentage}%"
)

        if score >= 9:

            st.success(
                "Excellent Internship Readiness 🚀"
            )

        elif score >= 7:

            st.info(
                "Good Internship Readiness 👍"
            )

        else:

            st.warning(
                "Needs Improvement 📚"
            )