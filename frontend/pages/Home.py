"""Home: recommendations dashboard + quick Twin status."""

import streamlit as st

from components.header import render_header, require_auth, show_api_error
from services.api import (ApiError, generate_recommendations, get_twin,
                          list_recommendations, update_recommendation)

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
render_header("🏠 Home", "Your Twin at a glance and fresh recommendations.")
token, user = require_auth()

try:
    with st.spinner("Loading..."):
        twin = get_twin(token)
        recs = list_recommendations(token).get("recommendations", [])
except ApiError as exc:
    show_api_error(exc)
    st.stop()

summary = twin.get("summary", {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("Skills", summary.get("skills_count", 0), help="Skills tracked in your Twin")
c2.metric("Open gaps", summary.get("gaps_count", 0))
c3.metric("Avg level", f"{summary.get('avg_level', 0)}/5")
c4.metric("Readiness", f"{summary.get('readiness_score', 0)}/100")
st.divider()

st.subheader("✨ Recommendations")
if st.button("🔄 Regenerate from my Twin", use_container_width=False):
    try:
        with st.spinner("Matching your gaps to projects and roles..."):
            generate_recommendations(token)
        st.rerun()
    except ApiError as exc:
        show_api_error(exc)

if not recs:
    st.info("No recommendations yet. Click regenerate to match your Twin against projects and internships.")
else:
    by_kind: dict = {}
    for rec in recs:
        by_kind.setdefault(rec.get("kind", "other"), []).append(rec)
    for kind in ("project", "internship", "action"):
        items = [r for r in by_kind.get(kind, []) if r.get("status") == "suggested"]
        if not items:
            continue
        st.markdown(f"**{kind.title()}s**")
        for rec in items[:5]:
            detail = rec.get("detail", {}) or {}
            cols = st.columns([4, 1, 1])
            with cols[0]:
                extra = ""
                if detail.get("why"):
                    extra = f" — {detail['why']}"
                elif detail.get("missing_skills"):
                    extra = f" — missing: {', '.join(detail['missing_skills'])}"
                elif detail.get("detail"):
                    extra = f" — {detail['detail'][:120]}"
                st.write(f"• **{rec.get('title')}**{extra}")
            with cols[1]:
                if st.button("Accept", key=f"acc{rec['id']}"):
                    try:
                        update_recommendation(token, rec["id"], "accepted")
                        st.rerun()
                    except ApiError as exc:
                        show_api_error(exc)
            with cols[2]:
                if st.button("Dismiss", key=f"dis{rec['id']}"):
                    try:
                        update_recommendation(token, rec["id"], "dismissed")
                        st.rerun()
                    except ApiError as exc:
                        show_api_error(exc)
