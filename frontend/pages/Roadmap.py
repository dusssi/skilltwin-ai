"""Roadmap: personalized plan with persistent progress."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import ApiError, generate_roadmap, get_roadmap, update_roadmap_item

st.set_page_config(page_title="Career Roadmap", page_icon="🗺️", layout="wide")
render_header("🗺️ Career Roadmap", "Generated from your gaps — completing items grows your Twin.")
token, user = require_auth()

goal_override = st.text_input("Goal for a new roadmap (optional)")
if st.button("✨ Generate roadmap from my Twin", use_container_width=True):
    try:
        with st.spinner("Building your personalized roadmap..."):
            generate_roadmap(token, goal_override or None)
        st.rerun()
    except ApiError as exc:
        show_api_error(exc)

try:
    data = get_roadmap(token)
except ApiError as exc:
    show_api_error(exc)
    st.stop()

roadmap = data.get("roadmap")
items = data.get("items", [])
progress = data.get("progress", {})
if not roadmap:
    st.info("No roadmap yet. Generate one from your Twin above.")
    st.stop()

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("🎯 Goal", (roadmap.get("goal") or "—")[:30])
m2.metric("📋 Items", f"{progress.get('completed', 0)}/{progress.get('total', 0)}")
m3.metric("📊 Progress", f"{progress.get('percent', 0)}%")
st.progress(progress.get("percent", 0) / 100)
st.divider()

for item in items:
    status = item.get("status", "pending")
    icon = {"completed": "✅", "in_progress": "🔄", "pending": "⬜", "skipped": "⏭️"}.get(status, "⬜")
    with st.expander(f"{icon} {item.get('title')}  (`{status}`)", expanded=(status != "completed")):
        st.write(item.get("description", ""))
        st.caption(f"Skill: {item.get('skill') or '—'} • Difficulty: {item.get('difficulty')} • "
                   f"Effort: {item.get('estimated_effort')} • Priority: {item.get('priority')}")
        if item.get("dependencies"):
            st.caption("Depends on: " + ", ".join(item["dependencies"]))
        for resource in item.get("resources", []):
            st.write(f"🔗 {resource}")
        cols = st.columns(3)
        with cols[0]:
            if status != "in_progress" and st.button("Start", key=f"start{item['id']}"):
                try:
                    update_roadmap_item(token, item["id"], "in_progress")
                    st.rerun()
                except ApiError as exc:
                    show_api_error(exc)
        with cols[1]:
            if status != "completed" and st.button("Mark complete", key=f"done{item['id']}"):
                try:
                    with st.spinner("Recording evidence in your Twin..."):
                        result = update_roadmap_item(token, item["id"], "completed")
                    change = (result or {}).get("twin_change") or {}
                    if change:
                        st.success(f"Twin updated: {change.get('skill')} → level "
                                   f"{change.get('new_level')}")
                    st.rerun()
                except ApiError as exc:
                    show_api_error(exc)
        with cols[2]:
            if status not in {"completed", "skipped"} and st.button("Skip", key=f"skip{item['id']}"):
                try:
                    update_roadmap_item(token, item["id"], "skipped")
                    st.rerun()
                except ApiError as exc:
                    show_api_error(exc)
