import streamlit as st

from services.api import (
    run_runtime
)

st.set_page_config(
    page_title="Runtime Monitor",
    page_icon="⚙️",
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
        "⚙️ Runtime Monitor"
    )

    st.caption(
        "Observe → Plan → Act → Reflect → Replan"
    )

st.divider()

# ======================
# DASHBOARD METRICS
# ======================

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "🎯 Goal",
        "AI Internship"
    )

with m2:

    st.metric(
        "🤖 Agent",
        "Active"
    )

with m3:

    st.metric(
        "📊 Status",
        "Ready"
    )

st.divider()

# ======================
# AGENT CONFIGURATION
# ======================

st.subheader(
    "🚀 Agent Configuration"
)

user_id = st.text_input(
    "User ID",
    value="user123"
)

goal = st.text_input(
    "Goal",
    value="AI Internship"
)

if st.button(
    "Run Agent",
    use_container_width=True
):

    with st.spinner(
        "Running SkillTwin Agent..."
    ):

        result = run_runtime(
            user_id,
            goal
        )

    runtime = result[
        "result"
    ]

    completed = len(
        runtime[
            "completed_tasks"
        ]
    )

    st.divider()

    # ======================
    # EXECUTION METRICS
    # ======================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "✅ Status",
            result[
                "status"
            ]
        )

    with c2:

        st.metric(
            "🔄 Iterations",
            runtime[
                "iterations"
            ]
        )

    with c3:

        st.metric(
            "📋 Tasks",
            completed
        )

    st.divider()

    # ======================
    # TASKS
    # ======================

    st.subheader(
        "✅ Completed Tasks"
    )

    for task in runtime[
        "completed_tasks"
    ]:

        st.success(
            task
        )

    st.divider()

    # ======================
    # REFLECTION
    # ======================

    st.subheader(
        "🧠 Reflection Analysis"
    )

    reflection = runtime[
        "reflection"
    ]

    score = 0

    if isinstance(
        reflection,
        dict
    ):

        score = reflection.get(
            "score",
            0
        )

    reflection_col1, reflection_col2 = st.columns(
        2
    )

    with reflection_col1:

        st.metric(
            "Reflection Score",
            f"{score}/10"
        )

        st.progress(
            score / 10
        )

    with reflection_col2:

        if score >= 8:

            st.success(
                "Excellent Agent Performance 🚀"
            )

        elif score >= 6:

            st.info(
                "Good Agent Performance 👍"
            )

        else:

            st.warning(
                "Needs Improvement 📚"
            )

    st.json(
        reflection
    )

    st.divider()

    # ======================
    # OBSERVATIONS
    # ======================

    st.subheader(
        "👀 Agent Observations"
    )

    for observation in runtime[
        "observations"
    ]:

        st.info(
            observation
        )

    st.divider()

    # ======================
    # SUMMARY
    # ======================

    st.subheader(
        "📈 Runtime Summary"
    )

    st.success(
        f"""
        Goal: {goal}

        Iterations: {runtime['iterations']}

        Tasks Completed: {completed}

        Reflection Score: {score}/10
        """
    )

st.divider()

st.caption(
    "SkillTwin AI v1.0 • Autonomous Career Agent"
)