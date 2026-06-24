import streamlit as st

from services.api import (
    get_profile
)

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
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
        "👤 User Profile"
    )

    st.caption(
        "View your career profile, skills, projects and growth metrics."
    )

st.divider()

# ======================
# INPUT
# ======================

user_id = st.text_input(
    "User ID",
    value="user123"
)

load_profile = st.button(
    "Load Profile"
)

if load_profile:

    data = get_profile(
        user_id
    )

    profile = data[
        "profile"
    ]

    skills_count = len(
        profile["skills"]
    )

    missing_count = len(
        profile["missing_skills"]
    )

    projects_count = len(
        profile["projects"]
    )

    reflection_score = profile[
        "reflection_score"
    ]

    # ======================
    # METRICS
    # ======================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🧠 Skills",
            skills_count
        )

    with col2:

        st.metric(
            "⚠ Missing",
            missing_count
        )

    with col3:

        st.metric(
            "🚀 Projects",
            projects_count
        )

    with col4:

        st.metric(
            "📊 Reflection",
            reflection_score
        )

    st.divider()

    # ======================
    # GOAL
    # ======================

    st.subheader(
        "🎯 Career Goal"
    )

    st.success(
        profile[
            "primary_goal"
        ]
    )

    st.divider()

    # ======================
    # SKILLS + MISSING
    # ======================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🧠 Current Skills"
        )

        st.write(
            ", ".join(
                profile["skills"]
            )
        )

    with right:

        st.subheader(
            "⚠ Missing Skills"
        )

        st.write(
            ", ".join(
                profile[
                    "missing_skills"
                ]
            )
        )

    st.divider()

    # ======================
    # PROJECTS
    # ======================

    st.subheader(
        "🚀 Projects"
    )

    projects_col1, projects_col2, projects_col3 = st.columns(3)

    projects = profile[
        "projects"
    ]

    if len(projects) > 0:

        with projects_col1:

            st.info(
                projects[0]
            )

    if len(projects) > 1:

        with projects_col2:

            st.info(
                projects[1]
            )

    if len(projects) > 2:

        with projects_col3:

            st.info(
                projects[2]
            )

    st.divider()

    # ======================
    # REFLECTION
    # ======================

    st.subheader(
        "📈 Reflection Score"
    )

    st.metric(
        "Career Reflection Score",
        f"{reflection_score}/10"
    )

    st.progress(
        reflection_score / 10
    )

    if reflection_score >= 8:

        st.success(
            "Excellent Career Progress 🚀"
        )

    elif reflection_score >= 6:

        st.info(
            "Good Career Progress 👍"
        )

    else:

        st.warning(
            "Needs Improvement 📚"
        )

st.divider()

st.caption(
    "SkillTwin AI v1.0 • Profile Intelligence"
)