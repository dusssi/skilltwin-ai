"""SkillTwin AI — landing page and live Twin overview."""

import streamlit as st

from components.header import render_header, render_sidebar_auth, show_api_error
from services.api import ApiError, get_twin, health

st.set_page_config(page_title="SkillTwin AI", page_icon="🧠", layout="wide",
                   initial_sidebar_state="expanded")

render_header("SkillTwin AI", "Your evolving AI career twin — skills, gaps, roadmap, memory.")
user = render_sidebar_auth()

try:
    status = health()
except ApiError as exc:
    show_api_error(exc)
    st.stop()

st.caption(f"Backend: {status.get('status', '?')} • v{status.get('version', '?')} • "
           f"DB ready: {status.get('database_ready')} • "
           f"LLM: {'connected' if status.get('llm_configured') else 'local Twin mode'}")
st.divider()

token = st.session_state.get("token")
if not token or not user:
    st.subheader("What SkillTwin does")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("📄 Resume → Twin\n\nUpload a resume; skills, gaps and readiness update your Twin.")
        st.success("🎯 Gaps & Roadmap\n\nPersonalized gaps and a roadmap generated from them.")
    with col2:
        st.success("💬 Twin-aware Chat\n\nCareer coaching grounded in your real profile and memory.")
        st.success("🧠 Memory\n\nGoals, achievements and preferences persist across sessions.")
    with col3:
        st.success("⚙️ Agent Runs\n\nObserve → plan → act → reflect maintenance of your Twin.")
        st.success("🚀 Recommendations\n\nProjects and internships matched to your gaps.")
    st.divider()
    st.info("👈 Create an account or sign in from the sidebar to build your Skill Twin.")
    st.stop()

try:
    with st.spinner("Loading your Skill Twin..."):
        twin = get_twin(token)
except ApiError as exc:
    show_api_error(exc)
    st.stop()

summary = twin.get("summary", {})
profile = twin.get("profile", {})

m1, m2, m3, m4 = st.columns(4)
m1.metric("🧠 Skills tracked", summary.get("skills_count", 0))
m2.metric("🎯 Open gaps", summary.get("gaps_count", 0))
m3.metric("🚀 Projects", summary.get("projects_count", 0))
m4.metric("📊 Readiness", f"{summary.get('readiness_score', 0)}/100")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("🎯 Career direction")
    st.write(f"**Goal:** {profile.get('primary_goal') or '— not set —'}")
    st.write(f"**Target role:** {profile.get('target_role') or '— not set —'}")
    if summary.get("top_gaps"):
        st.write("**Top gaps:** " + ", ".join(summary["top_gaps"]))
    progress = summary.get("roadmap_progress") or {}
    if progress.get("total"):
        st.progress(progress.get("percent", 0) / 100,
                    text=f"Roadmap: {progress.get('completed', 0)}/{progress.get('total', 0)} done")
    else:
        st.caption("No roadmap yet — generate one from the Roadmap page.")
with right:
    st.subheader("🕓 Recent Twin activity")
    events = summary.get("recent_events", [])
    if not events:
        st.caption("No activity yet. Upload a resume or chat to get started.")
    for event in events[:6]:
        st.write(f"- `{event.get('type')}` — {str(event.get('data'))[:100]}")

st.divider()
st.caption("SkillTwin AI v2.0 • Use the sidebar pages: Home, Chat, Profile, Resume, Roadmap, Runtime.")
