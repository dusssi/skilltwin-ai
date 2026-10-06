"""Shared page header + sidebar auth (used by every page)."""

import streamlit as st

from services.api import ApiError, login, logout, register


def render_header(title: str, caption: str) -> None:
    header_col1, header_col2 = st.columns([1, 4])
    with header_col1:
        try:
            st.image("assets/logo.png", width=110)
        except Exception:
            st.markdown("### 🧠")
    with header_col2:
        st.title(title)
        st.caption(caption)
    st.divider()


def _do_login(username: str, password: str) -> None:
    data = login(username, password)
    st.session_state.token = data["token"]
    st.session_state.user = data["user"]
    st.rerun()


def _do_register(username: str, password: str, display_name: str) -> None:
    data = register(username, password, display_name)
    st.session_state.token = data["token"]
    st.session_state.user = data["user"]
    st.rerun()


def render_sidebar_auth() -> dict | None:
    """Render auth controls in the sidebar. Returns the user dict or None."""
    st.sidebar.header("🔐 Account")
    user = st.session_state.get("user")
    token = st.session_state.get("token")
    if user and token:
        st.sidebar.success(f"Signed in as **{user.get('username', '')}**")
        if st.sidebar.button("Logout", use_container_width=True):
            try:
                logout(token)
            except ApiError:
                pass
            st.session_state.pop("token", None)
            st.session_state.pop("user", None)
            st.rerun()
        return user

    tab_login, tab_register = st.sidebar.tabs(["Login", "Register"])
    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.sidebar.error("Enter username and password.")
            else:
                try:
                    with st.spinner("Signing in..."):
                        _do_login(username, password)
                except ApiError as exc:
                    st.sidebar.error(exc.message)
    with tab_register:
        new_user = st.text_input("Username", key="reg_user")
        display = st.text_input("Display name", key="reg_display")
        new_pass = st.text_input("Password (min 8 chars)", type="password", key="reg_pass")
        if st.button("Create account", use_container_width=True):
            if not new_user or not new_pass:
                st.sidebar.error("Enter username and password.")
            else:
                try:
                    with st.spinner("Creating account..."):
                        _do_register(new_user, new_pass, display or new_user)
                except ApiError as exc:
                    st.sidebar.error(exc.message)
    return None


def require_auth():
    """Stop the page with guidance when the user is not signed in."""
    user = render_sidebar_auth()
    if not user or not st.session_state.get("token"):
        st.info("👈 Sign in or create an account in the sidebar to use SkillTwin.")
        st.stop()
    return st.session_state.token, user


def show_api_error(exc: ApiError) -> None:
    if exc.status == 0:
        st.error(f"⚠️ Backend unavailable: {exc.message}")
    elif exc.status == 401:
        st.session_state.pop("token", None)
        st.session_state.pop("user", None)
        st.error("Session expired. Please sign in again from the sidebar.")
    else:
        st.error(f"Error ({exc.status}): {exc.message}")
