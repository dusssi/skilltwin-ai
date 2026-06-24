import streamlit as st


def render_header(
    title: str,
    caption: str
):

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
            title
        )

        st.caption(
            caption
        )

    st.divider()