import streamlit as st
import yaml
from config import set_page_config
from forms import render_prediction_form
from streamlit_authenticator import Authenticate
set_page_config()

# Charger la configuration d'authentification
with open("auth/config_auth.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

# Initialiser l'authentificateur
authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Sélection de la langue (fr par défaut)
lang = st.sidebar.selectbox("Language", ["Français", "English"])
lang_code = "en" if lang == "English" else "fr"
translations = load_translations(lang_code)

# Formulaire de login
authenticator.login()

if st.session_state.get("authentication_status"):
    authenticator.logout(location="sidebar")
    st.title(translations["title"])
    st.write(translations["subtitle"])
    st.write(translations["welcome_message"].format(name=st.session_state.get("name")))

    # Formulaire de prédiction
    render_prediction_form(translations)

elif st.session_state.get("authentication_status") is False:
    st.error(translations["incorrect_credentials"])
elif st.session_state.get("authentication_status") is None:
    st.warning(translations["login_prompt"])
