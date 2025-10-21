from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_st():
    st_mock = MagicMock()
    st_mock.session_state = {
        "selected_client_id": 1,
        "page": None,
        "show_delete_modal": False,
        "show_prediction_modal": False,
        "score_data": None,
        "edit_client_id": None,
    }
    st_mock.error = MagicMock()
    st_mock.columns.side_effect = (
        lambda n: [MagicMock(), MagicMock()] if n == 2 else [MagicMock(), MagicMock(), MagicMock()]
    )
    st_mock.subheader = MagicMock()
    st_mock.write = MagicMock()
    st_mock.markdown = MagicMock()
    st_mock.divider = MagicMock()
    st_mock.button = MagicMock(return_value=False)
    st_mock.spinner = MagicMock()
    st_mock.rerun = MagicMock()
    return st_mock


@pytest.fixture
def mock_translations():
    return {
        "client_not_found": "Client non trouvé",
        "back_to_list": "Retour à la liste",
        "client_details_title": "Détails du client",
        "personal_information": "Informations personnelles",
        "nom": "Nom",
        "date_naissance": "Date de naissance",
        "telephone": "Téléphone",
        "email": "Email",
        "adresse": "Adresse",
        "prediction_data": "Données de prédiction",
        "regional_real_estate_information": "Informations immobilières régionales",
        "REG_CITY_NOT_LIVE_CITY": "Ville de résidence ≠ ville d'enregistrement",
        "NAME_INCOME_TYPE": "Type de revenu",
        "NAME_HOUSING_TYPE": "Type de logement",
        "DAYS_LAST_PHONE_CHANGE": "Jours depuis le dernier changement de téléphone",
        "DAYS_ID_PUBLISH": "Jours depuis la publication de l'identifiant",
        "REG_CITY_NOT_WORK_CITY": "Ville de résidence ≠ ville de travail",
        "FLAG_EMP_PHONE": "Téléphone professionnel",
        "NAME_EDUCATION_TYPE": "Niveau d'éducation",
        "DAYS_REGISTRATION": "Jours depuis l'enregistrement",
        "FLAG_DOCUMENT_3": "Document 3",
        "EXT_SOURCE_1": "Source externe 1",
        "EXT_SOURCE_2": "Source externe 2",
        "EXT_SOURCE_3": "Source externe 3",
        "YEARS_BEGINEXPLUATATION_AVG": "Années d'exploitation moyennes",
        "ELEVATORS_AVG": "Ascenseurs moyens",
        "FLOORSMIN_AVG": "Étage minimum moyen",
        "HOUSETYPE_MODE": "Type de maison",
        "EMERGENCYSTATE_MODE": "État d'urgence",
        "YEARS_BUILD_AVG": "Années de construction moyennes",
        "ENTRANCES_AVG": "Entrées moyennes",
        "FLOORSMAX_AVG": "Étage maximum moyen",
        "WALLSMATERIAL_MODE": "Matériau des murs",
        "REGION_RATING_CLIENT": "Notation régionale du client",
        "delete": "Supprimer",
        "calculate_prediction": "Calculer la prédiction",
        "calculating_score": "Calcul du score en cours...",
        "edit": "Modifier",
    }


@pytest.fixture
def mock_client():
    return {
        "id": 1,
        "nom": "Berna",
        "prenom": "Micha",
        "date_naissance": "1980-01-01",
        "age": 43,
        "telephone": "0612345678",
        "email": "michaberna@neobanque.com",
        "adresse": "123 Rue de Paris, 75000 Paris",
        "REG_CITY_NOT_LIVE_CITY": 0,
        "NAME_INCOME_TYPE": "Salarié",
        "DAYS_EMPLOYED": 10,
        "NAME_HOUSING_TYPE": "Appartement",
        "DAYS_LAST_PHONE_CHANGE": 365,
        "DAYS_ID_PUBLISH": 100,
        "REG_CITY_NOT_WORK_CITY": 0,
        "FLAG_EMP_PHONE": 1,
        "NAME_EDUCATION_TYPE": "Supérieur",
        "DAYS_REGISTRATION": 1000,
        "FLAG_DOCUMENT_3": 1,
        "EXT_SOURCE_1": 0.5,
        "EXT_SOURCE_2": 0.3,
        "EXT_SOURCE_3": 0.7,
        "YEARS_BEGINEXPLUATATION_AVG": 10,
        "ELEVATORS_AVG": 1,
        "FLOORSMIN_AVG": 1,
        "HOUSETYPE_MODE": "Appartement",
        "EMERGENCYSTATE_MODE": "Non",
        "YEARS_BUILD_AVG": 20,
        "ENTRANCES_AVG": 2,
        "FLOORSMAX_AVG": 5,
        "WALLSMATERIAL_MODE": "Brique",
        "REGION_RATING_CLIENT": 1,
    }


@pytest.fixture
def mock_render_data_field():
    mock = MagicMock()
    return mock


def test_render_client_details_client_not_found(mock_st, mock_translations):
    with patch.multiple("forms.client_details", st=mock_st, get_client=lambda _: None):
        from forms.client_details import render_client_details

        render_client_details(mock_translations)
        mock_st.error.assert_called_once_with(mock_translations["client_not_found"])


def test_back_to_list_button(mock_st, mock_translations, mock_client):
    def button_side_effect(*args, **kwargs):
        if kwargs.get("key") == "back_to_list":
            mock_st.session_state["page"] = "client_list"
            return True
        return False

    mock_st.button.side_effect = button_side_effect

    with patch.multiple(
        "forms.client_details",
        st=mock_st,
        get_client=lambda _: mock_client,
        render_data_field=MagicMock(),
    ):
        from forms.client_details import render_client_details

        render_client_details(mock_translations)
        assert mock_st.session_state["page"] == "client_list"
        mock_st.rerun.assert_called_once()


def test_delete_button(mock_st, mock_translations, mock_client):
    def button_side_effect(*args, **kwargs):
        if kwargs.get("key") == "delete_button":
            mock_st.session_state["show_delete_modal"] = True
            return True
        return False

    mock_st.button.side_effect = button_side_effect

    with patch.multiple(
        "forms.client_details",
        st=mock_st,
        get_client=lambda _: mock_client,
        render_data_field=MagicMock(),
        render_delete_modal=MagicMock(),
    ):
        from forms.client_details import render_client_details

        render_client_details(mock_translations)
        assert mock_st.session_state["show_delete_modal"] is True
        mock_st.rerun.assert_called_once()


def test_calculate_prediction_button(mock_st, mock_translations, mock_client):
    def button_side_effect(*args, **kwargs):
        if kwargs.get("key") == "calculate_score_button":
            mock_st.session_state["show_prediction_modal"] = True
            mock_st.session_state["score_data"] = {"score": 0.85}
            return True
        return False

    mock_st.button.side_effect = button_side_effect

    with patch.multiple(
        "forms.client_details",
        st=mock_st,
        get_client=lambda _: mock_client,
        call_predict_api=lambda _: {"score": 0.85},
        render_data_field=MagicMock(),
        render_prediction_modal=MagicMock(),
    ):
        from forms.client_details import render_client_details

        render_client_details(mock_translations)
        assert mock_st.session_state["show_prediction_modal"] is True
        assert mock_st.session_state["score_data"] == {"score": 0.85}
        mock_st.rerun.assert_called_once()


def test_edit_button(mock_st, mock_translations, mock_client):
    def button_side_effect(*args, **kwargs):
        if kwargs.get("key") == "edit_button":
            mock_st.session_state["page"] = "edit_client"
            mock_st.session_state["edit_client_id"] = mock_client["id"]
            return True
        return False

    mock_st.button.side_effect = button_side_effect

    with patch.multiple(
        "forms.client_details",
        st=mock_st,
        get_client=lambda _: mock_client,
        render_data_field=MagicMock(),
    ):
        from forms.client_details import render_client_details

        render_client_details(mock_translations)
        assert mock_st.session_state["page"] == "edit_client"
        assert mock_st.session_state["edit_client_id"] == mock_client["id"]
        mock_st.rerun.assert_called_once()
