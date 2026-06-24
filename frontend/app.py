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

st.caption(
    "Your AI Career Growth Companion"
)

user_id = st.text_input(

    "User ID",

    value="user123"
)

if st.button(
    "Load Dashboard"
):

    data = get_profile(
        user_id
    )

    profile = data[
        "profile"
    ]

    st.divider()

    st.subheader(
        "🎯 Career Goal"
    )

    st.success(
        profile[
            "primary_goal"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Skills",

            len(
                profile[
                    "skills"
                ]
            )
        )

    with col2:

        st.metric(

            "Missing Skills",

            len(
                profile[
                    "missing_skills"
                ]
            )
        )

    with col3:

        st.metric(

            "Projects",

            len(
                profile[
                    "projects"
                ]
            )
        )

    with col4:

        st.metric(

            "Reflection Score",

            profile[
                "reflection_score"
            ]
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🧠 Current Skills"
        )

        for skill in profile[
            "skills"
        ]:

            st.success(
                skill
            )

    with right:

        st.subheader(
            "⚠️ Missing Skills"
        )

        for skill in profile[
            "missing_skills"
        ]:

            st.warning(
                skill
            )

    st.divider()

    st.subheader(
        "🚀 Projects"
    )

    for project in profile[
        "projects"
    ]:

        st.info(
            project
        )