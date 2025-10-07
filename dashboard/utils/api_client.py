import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("STREAMLIT_API_KEY")


def get_headers():
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def get_clients():
    try:
        response = requests.get(f"{API_URL}/clients/", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des clients : {str(e)}")
        return []


def get_client(client_id):
    try:
        response = requests.get(f"{API_URL}/clients/{client_id}", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération du client : {str(e)}")
        return None


def create_client(data):
    try:
        response = requests.post(
            f"{API_URL}/clients/", json=data, headers=get_headers(), timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la création du client : {str(e)}")
        return None


def update_client(client_id, data):
    try:
        response = requests.put(
            f"{API_URL}/clients/{client_id}", json=data, headers=get_headers(), timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour du client : {str(e)}")
        return None


def delete_client(client_id):
    try:
        response = requests.delete(
            f"{API_URL}/clients/{client_id}", headers=get_headers(), timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return False
    except Exception as e:
        st.error(f"Erreur lors de la suppression du client : {str(e)}")
        return False


def call_predict_api(data):
    try:
        response = requests.post(f"{API_URL}/predict", json=data, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {str(e)}")
        return None
