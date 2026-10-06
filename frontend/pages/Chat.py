"""Chat: Twin-aware career coaching with persistent sessions."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import ApiError, chat, chat_sessions, session_messages

st.set_page_config(page_title="AI Career Coach", page_icon="💬", layout="wide")
render_header("💬 AI Career Coach", "Grounded in your Twin, gaps, memory and progress.")
token, user = require_auth()

try:
    sessions = chat_sessions(token).get("sessions", [])
except ApiError as exc:
    show_api_error(exc)
    st.stop()

options = {"New conversation": None}
for session in sessions:
    label = (session.get("summary") or session["id"][:8])[:60] or session["id"][:8]
    options[f"{label} ({session.get('updated_at', '')[:10]})"] = session["id"]
choice = st.selectbox("Conversation", list(options.keys()))
active_session = options[choice]

history = []
if active_session:
    try:
        history = session_messages(token, active_session).get("messages", [])
    except ApiError as exc:
        show_api_error(exc)

for message in history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about your career, gaps, projects...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.spinner("SkillTwin is thinking..."):
            answer = chat(token, prompt, active_session)
        with st.chat_message("assistant"):
            st.markdown(answer["response"])
            if answer.get("fallback"):
                st.caption("ℹ️ Answered from your Twin directly (AI model unavailable).")
            for update in answer.get("twin_updates", []):
                st.caption(f"📝 Twin updated: {update}")
        st.session_state["_last_session"] = answer["session_id"]
        st.rerun()
    except ApiError as exc:
        show_api_error(exc)
