from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_st():
    st_mock = MagicMock()
    st_mock.session_state = {"page": None, "edit_client_id": 1, "refresh_requested": False}
    st_mock.subheader = MagicMock()
    st_mock.columns = MagicMock(side_effect=lambda n: [MagicMock() for _ in range(n)])
    st_mock.markdown = MagicMock()
    st_mock.divider = MagicMock()
    st_mock.success = MagicMock()
    st_mock.rerun = MagicMock()
    st_mock.text_input = MagicMock(return_value="")

    # Configuration spécifique pour form_submit_button
    st_mock.form_submit_button = MagicMock()
    return st_mock


@pytest.fixture
def mock_translations():
    return {
        "create_client": "Créer un client",
        "edit_client": "Modifier un client",
        "personal_information": "Informations personnelles",
        "credit_information": "Informations de crédit",
        "regional_real_estate_information": "Informations immobilières régionales",
        "adresse": "Adresse",
        "adresse_placeholder": "Entrez l'adresse",
        "CODE_GENDER": "Genre",
        "nom": "Nom",
        "prenom": "Prénom",
        "telephone": "Téléphone",
        "email": "Email",
        "date_naissance": "Date de naissance",
        "REG_CITY_NOT_LIVE_CITY": "Ville de résidence ≠ ville d'enregistrement",
        "REG_CITY_NOT_WORK_CITY": "Ville de résidence ≠ ville de travail",
        "NAME_INCOME_TYPE": "Type de revenu",
        "DAYS_EMPLOYED": "Jours d'emploi",
        "NAME_EDUCATION_TYPE": "Niveau d'éducation",
        "NAME_HOUSING_TYPE": "Type de logement",
        "FLAG_EMP_PHONE": "Téléphone professionnel",
        "DAYS_LAST_PHONE_CHANGE": "Jours depuis le dernier changement de téléphone",
        "DAYS_REGISTRATION": "Jours depuis l'enregistrement",
        "FLAG_DOCUMENT_3": "Document 3",
        "EXT_SOURCE_1": "Source externe 1",
        "EXT_SOURCE_2": "Source externe 2",
        "EXT_SOURCE_3": "Source externe 3",
        "YEARS_BEGINEXPLUATATION_AVG": "Années d'exploitation moyennes",
        "YEARS_BUILD_AVG": "Années de construction moyennes",
        "ELEVATORS_AVG": "Ascenseurs moyens",
        "ENTRANCES_AVG": "Entrées moyennes",
        "FLOORSMAX_AVG": "Étage maximum moyen",
        "FLOORSMIN_AVG": "Étage minimum moyen",
        "HOUSETYPE_MODE": "Type de maison",
        "WALLSMATERIAL_MODE": "Matériau des murs",
        "EMERGENCYSTATE_MODE": "État d'urgence",
        "REGION_RATING_CLIENT": "Notation régionale du client",
        "cancel": "Annuler",
        "save": "Enregistrer",
        "create_success": "Client créé avec succès",
        "update_success": "Client mis à jour avec succès",
    }


@pytest.fixture
def mock_client():
    return {
        "id": 1,
        "CODE_GENDER": "M",
        "nom": "Berna",
        "prenom": "Micha",
        "telephone": "0612345678",
        "email": "micha.berna@neobanque.com",
        "date_naissance": "1980-01-01",
        "adresse": "123 Rue de Paris, 75000 Paris",
        "REG_CITY_NOT_LIVE_CITY": "0",
        "REG_CITY_NOT_WORK_CITY": "0",
        "NAME_INCOME_TYPE": "Working",
        "DAYS_EMPLOYED": 3650,
        "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_HOUSING_TYPE": "House / apartment",
        "FLAG_EMP_PHONE": "0",
        "DAYS_LAST_PHONE_CHANGE": 365,
        "DAYS_REGISTRATION": 1000,
        "FLAG_DOCUMENT_3": "0",
        "EXT_SOURCE_1": 0.5,
        "EXT_SOURCE_2": 0.3,
        "EXT_SOURCE_3": 0.7,
        "YEARS_BEGINEXPLUATATION_AVG": 10,
        "YEARS_BUILD_AVG": 20,
        "ELEVATORS_AVG": 1,
        "ENTRANCES_AVG": 2,
        "FLOORSMAX_AVG": 5,
        "FLOORSMIN_AVG": 1,
        "HOUSETYPE_MODE": "Block of flats",
        "WALLSMATERIAL_MODE": "Stone, brick",
        "EMERGENCYSTATE_MODE": "No",
        "REGION_RATING_CLIENT": 1,
    }


@pytest.fixture
def mock_render_input_field():
    with patch("utils.forms.render_input_field") as mock:
        mock.return_value = "test_value"
        yield mock


def test_render_client_form_create(mock_st, mock_translations, mock_render_input_field):
    with (
        patch("forms.client_form.st", mock_st),
        patch("forms.client_form.get_client_id", return_value=None),
        patch("utils.api_client.create_client", return_value=True),
        patch("utils.forms.render_input_field", mock_render_input_field),
        patch("utils.mappings.transform_data_for_backend", return_value={}),
    ):
        from forms.client_form import render_client_form

        render_client_form(mock_translations, is_update=False)
        mock_st.subheader.assert_called_once_with(
            mock_translations["create_client"], divider="blue"
        )


def test_render_client_form_edit(mock_st, mock_translations, mock_client, mock_render_input_field):
    with (
        patch("forms.client_form.st", mock_st),
        patch("utils.api_client.get_client", return_value=mock_client),
        patch("forms.client_form.get_client_id", return_value=1),
        patch("utils.api_client.update_client", return_value=True),
        patch("utils.forms.render_input_field", mock_render_input_field),
        patch("utils.mappings.transform_data_for_backend", return_value={}),
    ):
        from forms.client_form import render_client_form

        render_client_form(mock_translations, is_update=True)
        mock_st.subheader.assert_called_once_with(mock_translations["edit_client"], divider="blue")


def test_cancel_button_create(mock_st, mock_translations, mock_render_input_field):
    def form_submit_button_side_effect(label, **kwargs):
        if kwargs.get("key") == "cancel_button":
            mock_st.session_state["page"] = "client_list"
            return True
        return False

    mock_st.form_submit_button.side_effect = form_submit_button_side_effect

    with (
        patch("forms.client_form.st", mock_st),
        patch("forms.client_form.get_client_id", return_value=None),
        patch("utils.forms.render_input_field", mock_render_input_field),
        patch("utils.mappings.transform_data_for_backend", return_value={}),
    ):
        from forms.client_form import render_client_form

        render_client_form(mock_translations, is_update=False)
        assert mock_st.session_state["page"] == "client_list"
        mock_st.rerun.assert_called_once()


def test_cancel_button_edit(mock_st, mock_translations, mock_client, mock_render_input_field):
    def form_submit_button_side_effect(label, **kwargs):
        if kwargs.get("key") == "cancel_button":
            mock_st.session_state["page"] = "client_details"
            return True
        return False

    mock_st.form_submit_button.side_effect = form_submit_button_side_effect

    with (
        patch("forms.client_form.st", mock_st),
        patch("utils.api_client.get_client", return_value=mock_client),
        patch("forms.client_form.get_client_id", return_value=1),
        patch("utils.forms.render_input_field", mock_render_input_field),
        patch("utils.mappings.transform_data_for_backend", return_value={}),
    ):
        from forms.client_form import render_client_form

        render_client_form(mock_translations, is_update=True)
        assert mock_st.session_state["page"] == "client_details"
        mock_st.rerun.assert_called_once()
