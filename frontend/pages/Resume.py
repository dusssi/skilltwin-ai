import streamlit as st

from services.api import (
    analyze_resume
)

st.set_page_config(

    page_title="Resume Analyzer",

    page_icon="📄",

    layout="wide"
)

st.title(
    "📄 Resume Intelligence"
)

resume_text = st.text_area(

    "Paste Resume Content",

    height=300
)

if st.button(
    "Analyze Resume"
):

    result = (
        analyze_resume(
            resume_text
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

    st.metric(

        "Career Readiness Score",

        result[
            "readiness_score"
        ]
    )