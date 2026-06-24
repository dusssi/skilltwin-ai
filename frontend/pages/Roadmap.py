import streamlit as st

from services.api import (
    get_roadmap
)

st.set_page_config(
    page_title="Career Roadmap",
    page_icon="🗺️",
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
        "🗺️ Career Roadmap"
    )

    st.caption(
        "Generate a personalized learning and career growth roadmap."
    )

st.divider()

# ======================
# INPUT
# ======================

user_id = st.text_input(
    "User ID",
    value="user123"
)

if st.button(
    "Generate Roadmap",
    use_container_width=True
):

    data = get_roadmap(
        user_id
    )

    roadmap = data[
        "roadmap"
    ]

    goal = data[
        "goal"
    ]

    total_steps = len(
        roadmap
    )

    completed_steps = 0

    completion_percentage = (
        completed_steps / total_steps * 100
        if total_steps > 0
        else 0
    )

    # ======================
    # METRICS
    # ======================

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "🎯 Goal",
            goal
        )

    with m2:

        st.metric(
            "🗺️ Steps",
            total_steps
        )

    with m3:

        st.metric(
            "✅ Completed",
            completed_steps
        )

    with m4:

        st.metric(
            "📊 Progress",
            f"{completion_percentage:.0f}%"
        )

    st.divider()

    # ======================
    # GOAL
    # ======================

    st.subheader(
        "🎯 Career Goal"
    )

    st.success(
        goal
    )

    st.divider()

    # ======================
    # ROADMAP
    # ======================

    st.subheader(
        "🚀 Learning Path"
    )

    for index, step in enumerate(
        roadmap,
        start=1
    ):

        st.info(
            f"Step {index}: {step}"
        )

    st.divider()

    # ======================
    # PROGRESS
    # ======================

    st.subheader(
        "📈 Progress Tracker"
    )

    st.progress(
        completion_percentage / 100
    )

    st.info(
        f"{completed_steps} of {total_steps} steps completed."
    )

    if completion_percentage >= 80:

        st.success(
            "Excellent Progress 🚀"
        )

    elif completion_percentage >= 50:

        st.info(
            "Good Progress 👍"
        )

    else:

        st.warning(
            "Roadmap just started 📚"
        )

    st.divider()

    # ======================
    # SUMMARY
    # ======================

    st.subheader(
        "📋 Roadmap Summary"
    )

    st.success(
        f"""
        Goal: {goal}

        Total Steps: {total_steps}

        Current Progress: {completion_percentage:.0f}%
        """
    )

st.divider()

st.caption(
    "SkillTwin AI v1.0 • Career Roadmap Engine"
)