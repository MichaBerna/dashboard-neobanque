import streamlit as st
from utils.api_client import create_client, get_client, update_client
from utils.forms import render_input_field
from utils.mappings import transform_data_for_backend


def render_client_form(translations, is_update=False):
    client_id = st.session_state.get("edit_client_id") if is_update else None
    client_data = get_client(client_id) if is_update else {}
    client_data = client_data if client_data else {}

    st.subheader(
        translations["edit_client"] if is_update else translations["create_client"], divider="blue"
    )

    with st.form(key="client_form"):
        # Informations personnelles
        st.markdown("### " + translations["personal_information"])
        data = {}

        col1, col2, col3 = st.columns(3)
        data["CODE_GENDER"] = render_input_field(
            col1,
            translations,
            "CODE_GENDER",
            client_data,
            default="M",
            options=["M", "F"],
            input_type="select",
        )
        data["nom"] = render_input_field(
            col2, translations, "nom", client_data, default="", input_type="text"
        )
        data["prenom"] = render_input_field(
            col3, translations, "prenom", client_data, default="", input_type="text"
        )

        col4, col5, col6 = st.columns(3)
        data["telephone"] = render_input_field(
            col4, translations, "telephone", client_data, default="", input_type="text"
        )
        data["email"] = render_input_field(
            col5, translations, "email", client_data, default="", input_type="text"
        )
        data["date_naissance"] = render_input_field(
            col6, translations, "date_naissance", client_data, default="", input_type="date"
        )

        data["adresse"] = st.text_input(
            translations["adresse"],
            value=client_data.get("adresse", ""),
            placeholder=translations["adresse_placeholder"],
        )
        st.divider()

        # Informations personnelles de crédit
        st.markdown("### " + translations["credit_information"])

        col7, col8 = st.columns(2)
        data["REG_CITY_NOT_LIVE_CITY"] = render_input_field(
            col7,
            translations,
            "REG_CITY_NOT_LIVE_CITY",
            client_data,
            default="0",
            options=["1", "0"],
            input_type="select",
        )
        data["REG_CITY_NOT_WORK_CITY"] = render_input_field(
            col8,
            translations,
            "REG_CITY_NOT_WORK_CITY",
            client_data,
            default="0",
            options=["1", "0"],
            input_type="select",
        )

        col9, col10, col11, col12 = st.columns(4)
        data["NAME_INCOME_TYPE"] = render_input_field(
            col9,
            translations,
            "NAME_INCOME_TYPE",
            client_data,
            default="",
            options=[
                "Working",
                "State servant",
                "Pensioner",
                "Commercial associate",
                "Student",
                "Unemployed",
                "Businessman",
                "Maternity leave",
            ],
            input_type="select",
        )
        data["DAYS_EMPLOYED"] = render_input_field(
            col10, translations, "DAYS_EMPLOYED", client_data, default=0, input_type="number"
        )
        data["NAME_EDUCATION_TYPE"] = render_input_field(
            col11,
            translations,
            "NAME_EDUCATION_TYPE",
            client_data,
            default="",
            options=[
                "Secondary / secondary special",
                "Higher education",
                "Incomplete higher",
                "Lower secondary",
                "Academic degree",
            ],
            input_type="select",
        )
        data["NAME_HOUSING_TYPE"] = render_input_field(
            col12,
            translations,
            "NAME_HOUSING_TYPE",
            client_data,
            default="",
            options=[
                "House / apartment",
                "With parents",
                "Municipal apartment",
                "Rented apartment",
                "Office apartment",
                "Co-op apartment",
            ],
            input_type="select",
        )

        col13, col14, col15 = st.columns(3)
        data["FLAG_EMP_PHONE"] = render_input_field(
            col13,
            translations,
            "FLAG_EMP_PHONE",
            client_data,
            default="0",
            options=["1", "0"],
            input_type="select",
        )
        data["DAYS_LAST_PHONE_CHANGE"] = render_input_field(
            col14,
            translations,
            "DAYS_LAST_PHONE_CHANGE",
            client_data,
            default=0,
            input_type="number",
        )
        data["DAYS_REGISTRATION"] = render_input_field(
            col15, translations, "DAYS_REGISTRATION", client_data, default=0, input_type="number"
        )

        col16, col17 = st.columns(2)
        data["FLAG_DOCUMENT_3"] = render_input_field(
            col16,
            translations,
            "FLAG_DOCUMENT_3",
            client_data,
            default="0",
            options=["1", "0"],
            input_type="select",
        )
        data["DAYS_ID_PUBLISH"] = render_input_field(
            col17, translations, "DAYS_ID_PUBLISH", client_data, default=0, input_type="number"
        )

        col18, col19, col20 = st.columns(3)
        data["EXT_SOURCE_1"] = render_input_field(
            col18, translations, "EXT_SOURCE_1", client_data, default=0.0, input_type="number"
        )
        data["EXT_SOURCE_2"] = render_input_field(
            col19, translations, "EXT_SOURCE_2", client_data, default=0.0, input_type="number"
        )
        data["EXT_SOURCE_3"] = render_input_field(
            col20, translations, "EXT_SOURCE_3", client_data, default=0.0, input_type="number"
        )
        st.divider()

        # Informations régionales & immobilières de crédit
        st.markdown("### " + translations["regional_real_estate_information"])

        col21, col22 = st.columns(2)
        data["YEARS_BEGINEXPLUATATION_AVG"] = render_input_field(
            col21,
            translations,
            "YEARS_BEGINEXPLUATATION_AVG",
            client_data,
            default=0,
            input_type="number",
        )
        data["YEARS_BUILD_AVG"] = render_input_field(
            col22, translations, "YEARS_BUILD_AVG", client_data, default=0, input_type="number"
        )

        col23, col24 = st.columns(2)
        data["ELEVATORS_AVG"] = render_input_field(
            col23, translations, "ELEVATORS_AVG", client_data, default=0, input_type="number"
        )
        data["ENTRANCES_AVG"] = render_input_field(
            col24, translations, "ENTRANCES_AVG", client_data, default=0, input_type="number"
        )

        col25, col26 = st.columns(2)
        data["FLOORSMAX_AVG"] = render_input_field(
            col25, translations, "FLOORSMAX_AVG", client_data, default=0, input_type="number"
        )
        data["FLOORSMIN_AVG"] = render_input_field(
            col26, translations, "FLOORSMIN_AVG", client_data, default=0, input_type="number"
        )

        col27, col28 = st.columns(2)
        data["HOUSETYPE_MODE"] = render_input_field(
            col27,
            translations,
            "HOUSETYPE_MODE",
            client_data,
            default="",
            options=[
                "Block of flats",
                "Specific housing",
                "Terraced house",
                "Council house",
                "Co-op apartment",
                "Private house",
            ],
            input_type="select",
        )
        data["WALLSMATERIAL_MODE"] = render_input_field(
            col28,
            translations,
            "WALLSMATERIAL_MODE",
            client_data,
            default="",
            options=[
                "Stone, brick",
                "Wood, log",
                "Panel",
                "Monolithic",
                "Block",
                "Other",
                "Concrete",
                "Metal",
            ],
            input_type="select",
        )

        col29, col30 = st.columns(2)
        data["EMERGENCYSTATE_MODE"] = render_input_field(
            col29,
            translations,
            "EMERGENCYSTATE_MODE",
            client_data,
            default="",
            options=["No", "Yes"],
            input_type="select",
        )
        data["REGION_RATING_CLIENT"] = render_input_field(
            col30, translations, "REGION_RATING_CLIENT", client_data, default=0, input_type="number"
        )

        # Boutons d'action
        left, right = st.columns(2)
        with left:
            if st.form_submit_button(
                translations["cancel"],
                key="cancel_button",
                icon=":material/cancel:",
                width="stretch",
            ):
                st.session_state["page"] = "client_list" if not is_update else "client_details"
                st.rerun()

        with right:
            if st.form_submit_button(
                translations["save"], key="save_button", icon=":material/check:", width="stretch"
            ):
                backend_data = transform_data_for_backend(data)
                if is_update:
                    if update_client(client_id, backend_data):
                        st.success(translations["update_success"])
                        st.session_state["page"] = "client_details"
                        st.rerun()
                else:
                    if create_client(backend_data):
                        st.success(translations["create_success"])
                        st.session_state["page"] = "client_list"
                        st.session_state["refresh_requested"] = True
                        st.rerun()
