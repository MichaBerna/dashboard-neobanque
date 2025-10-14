import streamlit as st
from streamlit_modal import Modal


def render_prediction_modal(translations, score_data):
    modal = Modal(key="prediction_modal", title=translations["prediction_title"])
    with modal.container():
        is_approved = score_data["prediction"]
        probabilite = score_data["probabilite"] * 100
        seuil = score_data["seuil"] * 100

        if not is_approved:
            status_color = "red"
            status_text = translations["credit_disapproved"]
        else:
            status_color = "green"
            status_text = translations["credit_approved"]

        st.write(translations["probability_score"].format(probabilite=f"{probabilite:.2f}"))
        st.write(f"{translations['prediction'].format(seuil=seuil)} :{status_color}[{status_text}]")

        if st.button(translations["close_button"]):
            st.session_state["show_prediction_modal"] = False
            st.rerun()

    return modal
