import streamlit as st
from utils.translations import load_translations


def render_sidebar(authenticator, authentication_status):
    if authentication_status:
        username = st.session_state.get("name")
        st.sidebar.subheader(username, divider="blue")
        translations = render_language_selector()
        authenticator.logout(translations["logout"], "sidebar")
    else:
        translations = render_language_selector()

    return translations


def render_language_selector():
    lang = st.sidebar.selectbox(
        "Language", ["Français", "English"], key="language_selector", label_visibility="collapsed"
    )
    lang_code = "en" if lang == "English" else "fr"
    translations = load_translations(lang_code)
    return translations
