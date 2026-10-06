"""Profile: full Skill Twin — identity, proficiency, gaps, goals, projects."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import (ApiError, add_skill, create_goal, create_project, get_twin,
                          update_twin)

st.set_page_config(page_title="Skill Twin Profile", page_icon="👤", layout="wide")
render_header("👤 Skill Twin Profile", "Your persistent career state: proficiency, gaps and goals.")
token, user = require_auth()

try:
    with st.spinner("Loading Twin..."):
        twin = get_twin(token)
except ApiError as exc:
    show_api_error(exc)
    st.stop()

summary = twin.get("summary", {})
profile = twin.get("profile", {})

m1, m2, m3, m4 = st.columns(4)
m1.metric("🧠 Skills", summary.get("skills_count", 0))
m2.metric("🎯 Open gaps", summary.get("gaps_count", 0))
m3.metric("🚀 Projects", summary.get("projects_count", 0))
m4.metric("📊 Readiness", f"{summary.get('readiness_score', 0)}/100")
st.divider()

st.subheader("🎯 Career direction")
with st.form("direction"):
    goal = st.text_input("Primary goal", value=profile.get("primary_goal", ""))
    role = st.text_input("Target role", value=profile.get("target_role", ""))
    exp = st.number_input("Experience (years)", min_value=0.0, max_value=60.0,
                          value=float(profile.get("experience_years", 0) or 0), step=0.5)
    edu = st.text_input("Education", value=profile.get("education", ""))
    if st.form_submit_button("Save"):
        try:
            with st.spinner("Saving..."):
                update_twin(token, {"primary_goal": goal, "target_role": role,
                                    "experience_years": exp, "education": edu})
            st.success("Twin updated.")
            st.rerun()
        except ApiError as exc:
            show_api_error(exc)
st.divider()

st.subheader("🧠 Skill proficiency")
skills = twin.get("skills", [])
if not skills:
    st.info("No skills yet. Upload a resume, chat about your skills, or add one below.")
else:
    for skill in sorted(skills, key=lambda s: s["level"], reverse=True):
        level, target = skill["level"], skill["target_level"]
        st.write(f"**{skill['skill_name']}** — level {level}/5 (target {target}) • "
                 f"confidence {int(skill.get('confidence', 0) * 100)}% • "
                 f"{len(skill.get('evidence', []))} evidence")
        st.progress(min(1.0, level / 5))
        with st.expander(f"Evidence & history: {skill['skill_name']}"):
            for ev in skill.get("evidence", []):
                st.write(f"- [{ev.get('source')}] {ev.get('note', '')} ({ev.get('at', '')[:10]})")
            for hist in skill.get("history", [])[:5]:
                st.write(f"- level {hist['old_level']} → {hist['new_level']}: "
                         f"{hist.get('reason', '')} [{hist.get('source', '')}]")

with st.form("add_skill"):
    st.markdown("**Add skill evidence manually**")
    name = st.text_input("Skill name")
    level = st.slider("Level", 1, 5, 2)
    note = st.text_input("Note (evidence)")
    if st.form_submit_button("Add"):
        try:
            add_skill(token, name, level, note)
            st.success(f"Recorded evidence for {name}.")
            st.rerun()
        except ApiError as exc:
            show_api_error(exc)
st.divider()

st.subheader("🎯 Skill gaps")
gaps = twin.get("gaps", [])
if not gaps:
    st.success("No open gaps against your target role. 🎉")
else:
    for gap in gaps:
        st.write(f"**{gap['skill_name']}** — {gap['current_level']}→{gap['target_level']} "
                 f"(`{gap['priority']}` priority)")
        st.caption(gap["reason"])
st.divider()

cols = st.columns(2)
with cols[0]:
    st.subheader("🏁 Goals")
    for goal_item in twin.get("goals", []):
        st.write(f"- **{goal_item['title']}** ({goal_item.get('target_role', '')}) — "
                 f"`{goal_item.get('status')}`")
    with st.form("add_goal"):
        title = st.text_input("New goal")
        grole = st.text_input("Goal target role")
        if st.form_submit_button("Add goal"):
            try:
                create_goal(token, title, grole)
                st.rerun()
            except ApiError as exc:
                show_api_error(exc)
with cols[1]:
    st.subheader("🚀 Projects")
    for project in twin.get("projects", []):
        st.write(f"- **{project['title']}** — `{project.get('status')}` "
                 f"({', '.join(project.get('skills', []))})")
    with st.form("add_project"):
        ptitle = st.text_input("Project title")
        pskills = st.text_input("Skills (comma separated)")
        if st.form_submit_button("Add project"):
            try:
                create_project(token, ptitle,
                               skills=[s.strip() for s in pskills.split(",") if s.strip()])
                st.rerun()
            except ApiError as exc:
                show_api_error(exc)
