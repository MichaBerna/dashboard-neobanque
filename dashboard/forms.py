import streamlit as st
from utils.api_client import call_predict_api


def render_prediction_form(translations):
    st.header(translations.get("prediction_title"))

    # Informations personnelles
    col = st.columns(1)
    with col[0]:
        code_gender = st.selectbox(
            translations.get("gender_label"),
            options=["M", "F"],
            help=translations.get("gender_help"),
        )

    # Bouton de soumission
    if st.button(translations.get("submit_button")):
        form_data = {
            "CODE_GENDER": code_gender,
        }
        response = call_predict_api(form_data)
        if response:
            st.success(
                translations["prediction_success"].format(
                    prediction=response["prediction"], probability=f"{response['probability']:.2f}"
                )
            )
        else:
            st.error(translations["prediction_error"])
