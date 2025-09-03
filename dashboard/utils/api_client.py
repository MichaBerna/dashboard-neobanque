import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")


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
