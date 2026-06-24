import streamlit as st

from services.api import (
    run_runtime
)

st.set_page_config(

    page_title="Runtime Monitor",

    page_icon="⚙️",

    layout="wide"
)

st.title(
    "⚙️ Runtime Monitor"
)

st.caption(
    "Observe → Plan → Act → Reflect → Replan"
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
    "Run Agent"
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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Status"
        )

        st.success(

            result[
                "status"
            ]
        )

    with col2:

        st.subheader(
            "Iterations"
        )

        st.metric(

            "Count",

            runtime[
                "iterations"
            ]
        )

    st.divider()

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

    st.subheader(
        "🧠 Reflection"
    )

    st.json(

        runtime[
            "reflection"
        ]
    )

    st.divider()

    st.subheader(
        "👀 Observations"
    )

    for observation in runtime[
        "observations"
    ]:

        st.info(
            observation
        )