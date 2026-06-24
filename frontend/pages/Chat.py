import streamlit as st

from services.api import (
    chat
)

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="💬",
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
        "💬 AI Career Coach"
    )

    st.caption(
        "Get personalized career guidance, internship advice, and learning recommendations."
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
        "🧠 Skills",
        "19"
    )

with m3:

    st.metric(
        "📊 Readiness",
        "80%"
    )

st.divider()

# ======================
# SUGGESTED QUESTIONS
# ======================

st.subheader(
    "🔥 Suggested Questions"
)

left, right = st.columns(2)

with left:

    st.info(
        "How do I get an AI Internship?"
    )

    st.info(
        "Which skills should I learn next?"
    )

with right:

    st.info(
        "What projects should I build?"
    )

    st.info(
        "How can I improve my resume?"
    )

st.divider()

# ======================
# CHAT INPUT
# ======================

user_id = st.text_input(
    "User ID",
    value="user123"
)

message = st.text_area(
    "Ask SkillTwin",
    placeholder="How do I get an AI Internship?"
)

if st.button(
    "Send Message",
    use_container_width=True
):

    if message:

        with st.spinner(
            "SkillTwin is thinking..."
        ):

            response = chat(
                user_id,
                message
            )

        st.divider()

        st.subheader(
            "🤖 SkillTwin Response"
        )

        st.success(
            response[
                "response"
            ]
        )

        st.divider()

        st.subheader(
            "📌 Next Suggested Actions"
        )

        st.info(
            """
            • Improve missing skills

            • Build portfolio projects

            • Update resume

            • Apply consistently

            • Track progress weekly
            """
        )

st.divider()

st.caption(
    "SkillTwin AI v1.0 • AI Career Coach"
)