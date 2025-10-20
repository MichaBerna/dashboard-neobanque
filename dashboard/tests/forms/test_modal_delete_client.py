from unittest.mock import MagicMock, patch

import pytest
from forms.modal_delete_client import render_delete_modal


@pytest.fixture
def mock_st():
    with patch("forms.modal_delete_client.st") as mock_st:
        mock_st.session_state = {}
        mock_left = MagicMock()
        mock_right = MagicMock()
        mock_st.columns.return_value = [mock_left, mock_right]
        yield mock_st


@pytest.fixture
def mock_modal():
    with patch("forms.modal_delete_client.Modal") as mock_modal_class:
        mock_modal_instance = MagicMock()
        mock_modal_class.return_value = mock_modal_instance
        yield mock_modal_class, mock_modal_instance


@pytest.fixture
def mock_delete_client():
    with patch("forms.modal_delete_client.delete_client") as mock_delete_client:
        yield mock_delete_client


def test_render_delete_modal(mock_st, mock_modal, mock_delete_client):
    mock_modal_class, mock_modal_instance = mock_modal

    translations = {
        "delete_confirmation": "Confirmation de suppression",
        "delete_confirmation_message": "Confirmez-vous la suppression du client"
        " {client_name} {client_surname} ?",
        "cancel": "Annuler",
        "confirm_delete": "Confirmer la suppression",
        "delete_success": "Client supprimé avec succès !",
    }
    client = {"id": 1, "nom": "Berna", "prenom": "Micha"}

    render_delete_modal(translations, client)

    mock_modal_class.assert_called_once_with(
        key="delete_modal", title="Confirmation de suppression"
    )
    mock_modal_instance.container.assert_called_once()
    mock_st.text.assert_called_once_with("Confirmez-vous la suppression du client Berna Micha ?")
    mock_st.columns.assert_called_once_with(2)


def test_render_delete_modal_cancel(mock_st, mock_modal, mock_delete_client):
    translations = {
        "delete_confirmation": "Confirmation de suppression",
        "delete_confirmation_message": "Confirmez-vous la suppression du client"
        " {client_name} {client_surname} ?",
        "cancel": "Annuler",
        "confirm_delete": "Confirmer la suppression",
        "delete_success": "Client supprimé avec succès !",
    }
    client = {"id": 1, "nom": "Berna", "prenom": "Micha"}

    mock_st.button.return_value = True

    render_delete_modal(translations, client)

    mock_st.button.assert_any_call(
        "Annuler", key="cancel_delete_button", icon=":material/cancel:", width="stretch"
    )
    assert mock_st.session_state["show_delete_modal"] is False
    mock_st.rerun.assert_called()


def test_render_delete_modal_confirm(mock_st, mock_modal, mock_delete_client):
    translations = {
        "delete_confirmation": "Confirmation de suppression",
        "delete_confirmation_message": "Confirmez-vous la suppression du clienté"
        " {client_name} {client_surname} ?",
        "cancel": "Annuler",
        "confirm_delete": "Confirmer la suppression",
        "delete_success": "Client supprimé avec succès !",
    }
    client = {"id": 1, "nom": "Berna", "prenom": "Micha"}

    mock_delete_client.return_value = True
    mock_st.button.side_effect = [False, True]

    render_delete_modal(translations, client)

    mock_st.button.assert_any_call(
        "Confirmer la suppression",
        key="confirm_delete_button",
        type="primary",
        icon=":material/delete:",
        width="stretch",
    )

    mock_delete_client.assert_called_once_with(1)
    mock_st.success.assert_called_once_with("Client supprimé avec succès !")
    assert mock_st.session_state["page"] == "client_list"
    assert mock_st.session_state["refresh_requested"] is True
    assert mock_st.rerun.call_count == 1
