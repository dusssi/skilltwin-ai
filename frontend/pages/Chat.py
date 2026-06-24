import streamlit as st

from services.api import (
    chat
)

st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide"
)

st.title(
    "💬 SkillTwin AI Chat"
)

user_id = st.text_input(
    "User ID",
    value="user123"
)

message = st.text_area(
    "Ask SkillTwin",
    placeholder="How do I get an AI Internship?"
)

if st.button(
    "Send"
):

    if message:

        response = chat(
            user_id,
            message
        )

        st.subheader(
            "🤖 Response"
        )

        st.write(
            response[
                "response"
            ]
        )