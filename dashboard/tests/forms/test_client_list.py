from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


@pytest.fixture
def mock_st():
    st_mock = MagicMock()
    st_mock.session_state = {"refresh_requested": False, "page": None, "selected_client_id": None}
    st_mock.subheader = MagicMock()
    st_mock.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
    st_mock.button = MagicMock(return_value=False)
    st_mock.warning = MagicMock()
    st_mock.rerun = MagicMock()
    return st_mock


@pytest.fixture
def mock_translations():
    return {
        "client_list_title": "Liste des clients",
        "refresh_list": "Rafraîchir la liste",
        "create_client_button": "Créer un client",
        "no_clients": "Aucun client trouvé",
        "id": "ID",
        "nom": "Nom",
        "prenom": "Prénom",
        "age": "Âge",
        "telephone": "Téléphone",
        "email": "Email",
    }


@pytest.fixture
def mock_clients():
    return [
        {
            "id": 1,
            "nom": "Berna",
            "prenom": "Micha",
            "age": 43,
            "telephone": "0612345678",
            "email": "micha.berna@neobanque.com",
        },
        {
            "id": 2,
            "nom": "Bowie",
            "prenom": "David",
            "age": 35,
            "telephone": "0687654321",
            "email": "david.bowie@neobanque.com",
        },
    ]


@pytest.fixture
def mock_aggrid():
    mock = MagicMock()
    mock.return_value = {
        "data": pd.DataFrame(
            [
                {
                    "id": 1,
                    "nom": "Berna",
                    "prenom": "Micha",
                    "age": 43,
                    "telephone": "0612345678",
                    "email": "Micha.Berna@example.com",
                },
                {
                    "id": 2,
                    "nom": "Martin",
                    "prenom": "Marie",
                    "age": 35,
                    "telephone": "0687654321",
                    "email": "marie.martin@example.com",
                },
            ]
        ),
        "selected_rows": pd.DataFrame(
            [
                {
                    "id": 1,
                    "nom": "Berna",
                    "prenom": "Micha",
                    "age": 43,
                    "telephone": "0612345678",
                    "email": "Micha.Berna@example.com",
                }
            ]
        ),
    }
    return mock


@pytest.fixture
def mock_grid_options_builder():
    mock = MagicMock()
    mock.from_dataframe.return_value = mock
    mock.configure_pagination.return_value = mock
    mock.configure_side_bar.return_value = mock
    mock.configure_default_column.return_value = mock
    mock.configure_column.return_value = mock
    mock.configure_selection.return_value = mock
    mock.build.return_value = {}
    return mock


def test_render_client_list_no_clients(mock_st, mock_translations):
    with (
        patch("forms.client_list.st", mock_st),
        patch("utils.api_client.get_clients", return_value=[]),
    ):
        from forms.client_list import render_client_list

        render_client_list(mock_translations)
        mock_st.warning.assert_called_once_with(mock_translations["no_clients"])


def test_render_client_list_with_clients(
    mock_st, mock_translations, mock_clients, mock_aggrid, mock_grid_options_builder
):
    with (
        patch("forms.client_list.st", mock_st),
        patch("utils.api_client.get_clients", return_value=mock_clients),
    ):
        import forms.client_list as cl

        cl.AgGrid = mock_aggrid
        cl.GridOptionsBuilder = lambda *args, **kwargs: mock_grid_options_builder

        cl.render_client_list(mock_translations)

        mock_st.subheader.assert_called_once_with(
            mock_translations["client_list_title"], divider="blue"
        )
        assert mock_aggrid.called or mock_aggrid.return_value is not None


def test_create_client_button(mock_st, mock_translations, mock_clients):
    def button_side_effect(*args, **kwargs):
        if kwargs.get("key") == "create_client_button":
            mock_st.session_state["page"] = "new_client"
            return True
        return False

    mock_st.button.side_effect = button_side_effect

    with (
        patch("forms.client_list.st", mock_st),
        patch("utils.api_client.get_clients", return_value=mock_clients),
        patch("forms.client_list.AgGrid", MagicMock()),
        patch("forms.client_list.GridOptionsBuilder", MagicMock()),
    ):
        from forms.client_list import render_client_list

        render_client_list(mock_translations)
        assert mock_st.session_state["page"] == "new_client"
        mock_st.rerun.assert_called_once()
