import streamlit as st

from services.api import (
    get_profile
)

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
    layout="wide"
)

st.title(
    "👤 User Profile"
)

user_id = st.text_input(
    "User ID",
    value="user123"
)

if st.button(
    "Load Profile"
):

    data = get_profile(
        user_id
    )

    profile = data[
        "profile"
    ]

    st.subheader(
        "Primary Goal"
    )

    st.success(
        profile[
            "primary_goal"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Skills"
        )

        for skill in profile[
            "skills"
        ]:

            st.success(
                skill
            )

    with col2:

        st.subheader(
            "Missing Skills"
        )

        for skill in profile[
            "missing_skills"
        ]:

            st.warning(
                skill
            )

    st.subheader(
        "Projects"
    )

    for project in profile[
        "projects"
    ]:

        st.info(
            project
        )

    st.metric(

        "Reflection Score",

        profile[
            "reflection_score"
        ]
    )