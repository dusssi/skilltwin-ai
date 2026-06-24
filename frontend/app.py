import streamlit as st

st.set_page_config(
    page_title="SkillTwin AI",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>

    .subtitle {
        font-size:18px;
        color:#9ca3af;
        margin-bottom:10px;
    }

    .footer {
        text-align:center;
        color:#9ca3af;
        padding-top:20px;
    }

    </style>
    """,
    unsafe_allow_html=True
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
        "SkillTwin AI"
    )

    st.caption(
        "AI Career Growth Companion"
    )

st.divider()

# ======================
# DASHBOARD METRICS
# ======================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "🧠 Skills",
        "19"
    )

with metric2:

    st.metric(
        "⚠ Missing",
        "2"
    )

with metric3:

    st.metric(
        "🚀 Projects",
        "3"
    )

with metric4:

    st.metric(
        "📊 Readiness",
        "80%"
    )

st.divider()

# ======================
# FEATURES
# ======================

st.subheader(
    "✨ Platform Features"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        "📄 Resume Intelligence"
    )

    st.success(
        "🎯 Internship Recommendations"
    )

with col2:

    st.success(
        "🗺️ Career Roadmaps"
    )

    st.success(
        "💬 AI Career Coach"
    )

with col3:

    st.success(
        "⚙️ Runtime Monitoring"
    )

    st.success(
        "📊 Readiness Analytics"
    )

st.divider()

# ======================
# QUICK ACTIONS
# ======================

st.subheader(
    "🚀 Quick Actions"
)

action1, action2, action3 = st.columns(3)

with action1:

    st.info(
        "📄 Analyze Resume"
    )

with action2:

    st.info(
        "🗺️ Generate Roadmap"
    )

with action3:

    st.info(
        "💬 Chat With SkillTwin"
    )

st.divider()

# ======================
# ABOUT
# ======================

left, right = st.columns(2)

with left:

    st.subheader(
        "📈 What SkillTwin Does"
    )

    st.write(
        """
        • Analyze resumes

        • Detect skill gaps

        • Recommend projects

        • Suggest internships

        • Generate roadmaps

        • Track career growth
        """
    )

with right:

    st.subheader(
        "🛠 Tech Stack"
    )

    st.write(
        """
        • Python

        • FastAPI

        • Streamlit

        • REST APIs

        • Pydantic

        • Resume Intelligence
        """
    )

st.divider()

st.markdown(
    """
    <div class="footer">
        SkillTwin AI v1.0 • AI Career Growth Companion
    </div>
    """,
    unsafe_allow_html=True
)