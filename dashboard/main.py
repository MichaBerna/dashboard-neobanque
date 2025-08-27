import requests
import streamlit as st

# URL de l'API déployée sur Render
API_URL = "https://api-neobanque.onrender.com/"

st.title("Dashboard Neobanque")
st.write("Ce dashboard appelle l'API Neobanque déployée sur Render.")

# Appel à l'endpoint racine (Hello World)
st.subheader("Endpoint Hello World")
if st.button("Appeler Hello World"):
    response = requests.get(f"{API_URL}/")
    if response.status_code == 200:
        st.success(f"Réponse : {response.json()}")
    else:
        st.error(f"Erreur : {response.status_code}")
