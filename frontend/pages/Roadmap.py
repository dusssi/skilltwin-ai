import streamlit as st

from services.api import (
    get_roadmap
)

st.set_page_config(
    page_title="Roadmap",
    page_icon="🗺️",
    layout="wide"
)

st.title(
    "🗺️ Career Roadmap"
)

user_id = st.text_input(
    "User ID",
    value="user123"
)

if st.button(
    "Generate Roadmap"
):

    data = get_roadmap(
        user_id
    )

    st.subheader(
        f"🎯 Goal: {data['goal']}"
    )

    roadmap = data[
        "roadmap"
    ]

    for index, step in enumerate(
        roadmap,
        start=1
    ):

        st.success(
            f"{index}. {step}"
        )