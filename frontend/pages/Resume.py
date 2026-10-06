"""Resume: upload/analyze and feed the Skill Twin."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import (ApiError, analyze_resume_text, resume_history, upload_resume)

st.set_page_config(page_title="Resume Intelligence", page_icon="📄", layout="wide")
render_header("📄 Resume Intelligence",
              "Analyze a resume — skills, gaps and projects flow into your Twin.")
token, user = require_auth()

tab_upload, tab_paste = st.tabs(["Upload PDF", "Paste text"])
result = None

with tab_upload:
    uploaded = st.file_uploader("Upload resume PDF (max 5 MB)", type=["pdf"])
    if uploaded and st.button("Analyze PDF", use_container_width=True):
        try:
            with st.spinner("Parsing PDF and updating your Twin..."):
                result = upload_resume(token, uploaded)
        except ApiError as exc:
            show_api_error(exc)

with tab_paste:
    text = st.text_area("Paste resume text", height=200)
    if st.button("Analyze text", use_container_width=True):
        if not text or len(text.strip()) < 20:
            st.error("Please paste at least a few lines of resume text.")
        else:
            try:
                with st.spinner("Analyzing and updating your Twin..."):
                    result = analyze_resume_text(token, text)
            except ApiError as exc:
                show_api_error(exc)

if result:
    analysis = result.get("analysis", {})
    diff = result.get("twin_diff", {})
    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Skills found", len(analysis.get("extracted_skills", [])))
    m2.metric("Missing (role)", len(analysis.get("missing_skills", [])))
    m3.metric("Twin skills added", len(diff.get("skills_added", [])))
    m4.metric("Readiness", f"{analysis.get('readiness_score', 0)}/100")
    st.progress(min(1.0, analysis.get("readiness_score", 0) / 100))
    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("✅ Extracted skills")
        st.write(", ".join(analysis.get("extracted_skills", [])) or "—")
        st.subheader("💼 Experience")
        exp = analysis.get("experience", {}) or {}
        st.write(f"{exp.get('years', 0)} yrs • {exp.get('seniority', '')} • "
                 f"{', '.join(exp.get('roles', []))}")
        st.subheader("🎓 Education")
        for edu in analysis.get("education", []):
            st.write(f"- {edu}")
    with right:
        st.subheader("⚠️ Missing for your role")
        st.write(", ".join(analysis.get("missing_skills", [])) or "—")
        st.subheader("📡 Career signals")
        for signal in analysis.get("career_signals", []):
            st.write(f"- {signal}")
    st.subheader("🚀 Projects detected & imported")
    for project in analysis.get("projects", [])[:10]:
        st.write(f"- **{project.get('title')}** ({', '.join(project.get('skills', []))})")

st.divider()
st.subheader("📚 Analysis history")
try:
    history = resume_history(token)
except ApiError as exc:
    show_api_error(exc)
    st.stop()
analyses = history.get("analyses", [])
if not analyses:
    st.caption("No resume analyses yet.")
for item in analyses[:10]:
    st.write(f"- {item.get('created_at', '')[:16]} — "
             f"{len(item.get('extracted_skills', []))} skills, "
             f"readiness {item.get('readiness_score', 0)}/100")
