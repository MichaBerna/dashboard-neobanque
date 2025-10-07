import streamlit as st
from streamlit_modal import Modal
from utils.api_client import delete_client


def render_delete_modal(translations, client):
    modal = Modal(key="delete_modal", title=translations["delete_confirmation"])
    with modal.container():
        st.text(
            translations["delete_confirmation_message"].format(
                client_name=client["nom"], client_surname=client["prenom"]
            )
        )

        # Boutons d'action
        left, right = st.columns(2)
        with left:
            if st.button(
                translations["cancel"],
                key="cancel_delete_button",
                icon=":material/cancel:",
                width="stretch",
            ):
                st.session_state["show_delete_modal"] = False
                st.rerun()
        with right:
            if st.button(
                translations["confirm_delete"],
                key="confirm_delete_button",
                type="primary",
                icon=":material/delete:",
                width="stretch",
            ) and delete_client(client["id"]):
                st.success(translations["delete_success"])
                st.session_state["page"] = "client_list"
                st.session_state["refresh_requested"] = True
                st.rerun()
