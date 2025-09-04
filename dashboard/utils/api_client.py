import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("STREAMLIT_API_KEY")


def call_predict_api(data):
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        response = requests.post(f"{API_URL}/predict", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {str(e)}")
        return None
