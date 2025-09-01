import json

import requests
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate

# URL de l'API déployée sur Render
API_URL = "https://api-neobanque.onrender.com/"

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


# Charger les traductions
def load_translations(lang):
    with open(f"locales/{lang}.json", encoding="utf-8") as tradfile:
        return json.load(tradfile)


translations = load_translations(lang_code)

# Afficher le formulaire de login
authenticator.login()

if st.session_state.get("authentication_status"):
    authenticator.logout(location="sidebar")
    st.title(translations["title"])
    st.write(translations["subtitle"])
    st.write(translations["welcome_message"].format(name=st.session_state.get("name")))

    # Appel à l'endpoint racine (Hello World)
    st.subheader("Endpoint Hello World")
    if st.button("Appeler Hello World"):
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success(f"Réponse : {response.json()}")
        else:
            st.error(f"Erreur : {response.status_code}")

elif st.session_state.get("authentication_status") is False:
    st.error(translations["incorrect_credentials"])
elif st.session_state.get("authentication_status") is None:
    st.warning(translations["login_prompt"])
