import streamlit as st
from forms.modal_delete_client import render_delete_modal
from utils.api_client import get_client


def render_client_details(translations):
    client_id = st.session_state.get("selected_client_id")
    client = get_client(client_id)

    if not client:
        st.error(translations["client_not_found"])
        return

    # Bouton de retour
    left, middle, right = st.columns(3)
    with left:
        if st.button(
            translations["back_to_list"],
            key="back_to_list",
            icon=":material/arrow_back:",
            width="stretch",
        ):
            st.session_state["page"] = "client_list"
            st.rerun()
    with middle:
        st.write("")
    with right:
        st.write("")

    st.subheader(translations["client_details_title"], divider="blue")

    # Informations personnelles
    st.subheader(translations["personal_information"])
    personal_info_col1, personal_info_col2 = st.columns(2)
    with personal_info_col1:
        st.markdown(f"**{translations['nom']}** : {client['nom']}")
        st.markdown(f"**{translations['prenom']}** : {client['prenom']}")
        st.markdown(f"**{translations['CODE_GENDER']}** : {client['CODE_GENDER']}")
        st.markdown(f"**{translations['date_naissance']}** : {client['date_naissance']}")
        st.markdown(f"**{translations['age']}** : {client['age']}")
    with personal_info_col2:
        st.markdown(f"**{translations['telephone']}** : {client['telephone']}")
        st.markdown(f"**{translations['email']}** : {client['email']}")
        st.markdown(f"**{translations['adresse']}** : {client['adresse']}")
    st.divider()

    # Données pour la prédiction
    st.subheader(translations["prediction_data"])
    prediction_col1, prediction_col2 = st.columns(2)
    with prediction_col1:
        st.markdown(f"**{translations['NAME_INCOME_TYPE']}** : {client['NAME_INCOME_TYPE']}")
        st.markdown(f"**{translations['NAME_EDUCATION_TYPE']}** : {client['NAME_EDUCATION_TYPE']}")
    with prediction_col2:
        st.markdown(f"**{translations['EXT_SOURCE_1']}** : {client['EXT_SOURCE_1']}")
        st.markdown(f"**{translations['EXT_SOURCE_2']}** : {client['EXT_SOURCE_2']}")
    st.divider()

    # Boutons d'action
    left, middle, right = st.columns(3)
    with left:
        if st.button(
            translations["delete"],
            key="delete_button",
            type="primary",
            icon=":material/delete:",
            width="stretch",
        ):
            st.session_state["show_delete_modal"] = True
            st.rerun()

    with middle:
        if st.button(
            translations["calculate_credit_score"],
            key="calculate_score_button",
            icon=":material/calculate:",
            width="stretch",
        ):
            st.session_state["page"] = "credit_score"
            st.rerun()

    with right:
        if st.button(
            translations["edit"], key="edit_button", icon=":material/edit:", width="stretch"
        ):
            st.session_state["page"] = "edit_client"
            st.rerun()

    # Modale de confirmation de suppression
    if st.session_state.get("show_delete_modal", False):
        render_delete_modal(translations, client)
