"""Runtime: run the SkillTwin agent (observe → plan → act → reflect)."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import ApiError, list_events, list_memory, run_runtime

st.set_page_config(page_title="Runtime Monitor", page_icon="⚙️", layout="wide")
render_header("⚙️ Runtime Monitor", "Observe → Plan → Act → Reflect → maintained Twin.")
token, user = require_auth()

goal = st.text_input("Goal for this agent run (optional — defaults to your Twin goal)")
if st.button("▶ Run SkillTwin agent", use_container_width=True):
    try:
        with st.spinner("Agent running: observing, planning, acting, reflecting..."):
            st.session_state["last_run"] = run_runtime(token, goal or None)
    except ApiError as exc:
        show_api_error(exc)

run = st.session_state.get("last_run")
if run:
    result = run.get("result", {})
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", run.get("status", ""))
    c2.metric("Steps", len(result.get("completed_steps", [])))
    c3.metric("Reflection", f"{(result.get('reflection') or {}).get('score', 0)}/10")
    st.success(result.get("summary", ""))
    st.divider()
    st.subheader("👀 Observations")
    for obs in result.get("observations", []):
        st.write(f"- {obs}")
    st.subheader("📋 Plan & completed steps")
    for step in (result.get("plan") or {}).get("steps", []):
        done = "✅" if step["name"] in result.get("completed_steps", []) else "⬜"
        st.write(f"{done} **{step['name']}** — {step.get('detail', '')} (`{step.get('agent')}`)")
    st.subheader("🧠 Reflection")
    reflection = result.get("reflection") or {}
    if reflection.get("issues"):
        st.write("**Issues:** " + "; ".join(reflection["issues"]))
    if reflection.get("suggestions"):
        st.write("**Suggestions:** " + "; ".join(reflection["suggestions"]))
    if reflection.get("narrative"):
        st.caption(reflection["narrative"])
    research = result.get("research") or {}
    if research.get("conclusion"):
        st.subheader("🔍 Research")
        st.write(research["conclusion"])
        for fact in (research.get("evidence") or [])[:10]:
            st.write(f"- {fact}")

st.divider()
cols = st.columns(2)
with cols[0]:
    st.subheader("🧠 Long-term memory")
    try:
        memories = list_memory(token).get("memories", [])
    except ApiError as exc:
        show_api_error(exc)
        memories = None
    if memories is not None:
        if not memories:
            st.caption("Nothing remembered yet — chat, upload a resume, or run the agent.")
        for mem in memories[:15]:
            st.write(f"- [{mem['kind']}] {mem['content']}")
with cols[1]:
    st.subheader("🕓 Progress events")
    try:
        events = list_events(token).get("events", [])
    except ApiError as exc:
        show_api_error(exc)
        events = None
    if events is not None:
        if not events:
            st.caption("No events yet.")
        for event in events[:15]:
            st.write(f"- `{event['event_type']}` {str(event.get('data'))[:120]}")
