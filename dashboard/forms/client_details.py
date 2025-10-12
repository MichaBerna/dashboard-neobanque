import streamlit as st
from forms.modal_delete_client import render_delete_modal
from utils.api_client import get_client
from utils.forms import render_data_field


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
    render_data_field(personal_info_col1, translations, "nom", client, client["prenom"])
    render_data_field(
        personal_info_col1, translations, "date_naissance", client, f"(âge : {client['age']})"
    )
    render_data_field(personal_info_col2, translations, "telephone", client)
    render_data_field(personal_info_col2, translations, "email", client)
    st.markdown(f"**{translations['adresse']}** : {client['adresse']}")
    st.divider()

    # Données pour la prédiction
    st.subheader(translations["prediction_data"])
    prediction_col1, prediction_col2 = st.columns(2)
    render_data_field(prediction_col1, translations, "REG_CITY_NOT_LIVE_CITY", client)
    render_data_field(
        prediction_col1,
        translations,
        "NAME_INCOME_TYPE",
        client,
        f"({client['DAYS_EMPLOYED']} ans)",
    )
    render_data_field(prediction_col1, translations, "NAME_HOUSING_TYPE", client)
    render_data_field(prediction_col1, translations, "DAYS_LAST_PHONE_CHANGE", client)
    render_data_field(prediction_col1, translations, "DAYS_ID_PUBLISH", client)
    render_data_field(prediction_col2, translations, "REG_CITY_NOT_WORK_CITY", client)
    render_data_field(prediction_col2, translations, "FLAG_EMP_PHONE", client)
    render_data_field(prediction_col2, translations, "NAME_EDUCATION_TYPE", client)
    render_data_field(prediction_col2, translations, "DAYS_REGISTRATION", client)
    render_data_field(prediction_col2, translations, "FLAG_DOCUMENT_3", client)

    ext_source1, ext_source2, ext_source3 = st.columns(3)
    render_data_field(ext_source1, translations, "EXT_SOURCE_1", client)
    render_data_field(ext_source2, translations, "EXT_SOURCE_2", client)
    render_data_field(ext_source3, translations, "EXT_SOURCE_3", client)
    st.divider()

    # Données pour la prédiction
    st.subheader(translations["regional_real_estate_information"])
    prediction_col1, prediction_col2 = st.columns(2)
    render_data_field(prediction_col1, translations, "YEARS_BEGINEXPLUATATION_AVG", client)
    render_data_field(prediction_col1, translations, "ELEVATORS_AVG", client)
    render_data_field(prediction_col1, translations, "FLOORSMIN_AVG", client)
    render_data_field(prediction_col1, translations, "HOUSETYPE_MODE", client)
    render_data_field(prediction_col1, translations, "EMERGENCYSTATE_MODE", client)
    render_data_field(prediction_col2, translations, "YEARS_BUILD_AVG", client)
    render_data_field(prediction_col2, translations, "ENTRANCES_AVG", client)
    render_data_field(prediction_col2, translations, "FLOORSMAX_AVG", client)
    render_data_field(prediction_col2, translations, "WALLSMATERIAL_MODE", client)
    render_data_field(prediction_col2, translations, "REGION_RATING_CLIENT", client)
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
