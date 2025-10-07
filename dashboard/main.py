import streamlit as st
import yaml
from config import set_page_config
from forms.client_details import render_client_details
from forms.client_form import render_client_form
from forms.client_list import render_client_list
from sidebar import render_sidebar
from streamlit_authenticator import Authenticate

set_page_config()

# Charger la configuration d'authentification
with open("auth/config_auth.yaml") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

# Formulaire de login
authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)
authenticator.login()

# Sidebar & translations
translations = render_sidebar(authenticator, st.session_state.get("authentication_status"))

# Pages & navigation
if st.session_state.get("authentication_status"):
    if "page" not in st.session_state:
        st.session_state["page"] = "client_list"

    if st.session_state["page"] == "client_list":
        render_client_list(translations)

    elif st.session_state["page"] == "client_details":
        render_client_details(translations)

    elif st.session_state["page"] == "edit_client":
        render_client_form(translations, is_update=True)

    elif st.session_state["page"] == "new_client":
        render_client_form(translations, is_update=False)

elif st.session_state.get("authentication_status") is False:
    st.error(translations["incorrect_credentials"])
elif st.session_state.get("authentication_status") is None:
    st.warning(translations["login_prompt"])
