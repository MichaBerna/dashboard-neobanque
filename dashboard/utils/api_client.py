import requests
import streamlit as st

API_URL = "https://api-neobanque.onrender.com/"


def call_predict_api(data):
    try:
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {str(e)}")
        return None
