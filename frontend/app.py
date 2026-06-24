import streamlit as st

from services.api import (
    get_profile
)

st.set_page_config(

    page_title="SkillTwin AI",

    page_icon="🚀",

    layout="wide"
)

st.title(
    "🚀 SkillTwin AI"
)

user_id = st.text_input(

    "User ID",

    value="user123"
)

if st.button(
    "Load Profile"
):

    profile_data = (
        get_profile(
            user_id
        )
    )

    profile = (
        profile_data[
            "profile"
        ]
    )

    st.subheader(
        "Career Goal"
    )

    st.write(
        profile[
            "primary_goal"
        ]
    )

    st.subheader(
        "Reflection Score"
    )

    st.metric(

        "Score",

        profile[
            "reflection_score"
        ]
    )

    st.subheader(
        "Skills"
    )

    st.write(

        profile[
            "skills"
        ]
    )

    st.subheader(
        "Missing Skills"
    )

    st.write(

        profile[
            "missing_skills"
        ]
    )

    st.subheader(
        "Projects"
    )

    st.write(

        profile[
            "projects"
        ]
    )