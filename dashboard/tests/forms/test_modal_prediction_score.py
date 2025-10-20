from unittest.mock import MagicMock, patch

import pytest
from forms.modal_prediction_score import render_prediction_modal


@pytest.fixture
def mock_st():
    with patch("forms.modal_prediction_score.st") as mock_st:
        mock_st.session_state = {}
        yield mock_st


@pytest.fixture
def mock_modal():
    with patch("forms.modal_prediction_score.Modal") as mock_modal_class:
        mock_modal_instance = MagicMock()
        mock_modal_class.return_value = mock_modal_instance
        yield mock_modal_class, mock_modal_instance


def test_render_prediction_modal_approved(mock_st, mock_modal):
    mock_modal_class, mock_modal_instance = mock_modal

    translations = {
        "prediction_title": "Score de crédit",
        "probability_score": "Le score de confiance calculé pour ce profil"
        " client est de {probabilite}%.",
        "prediction": "Cela est inférieur au seuil préconisé de {seuil}%, ",
        "credit_approved": "le risque de défaut de paiement est faible.",
        "credit_disapproved": "un risque de défaut de paiement existe.",
        "close_button": "Fermer",
    }
    score_data = {"prediction": True, "probabilite": 0.85, "seuil": 0.75}

    modal = render_prediction_modal(translations, score_data)

    assert modal == mock_modal_instance
    mock_modal_class.assert_called_once_with(key="prediction_modal", title="Score de crédit")
    mock_modal_instance.container.assert_called_once()

    mock_st.write.assert_any_call(
        "Le score de confiance calculé pour ce profil client est de 85.00%."
    )
    mock_st.write.assert_any_call(
        "Cela est inférieur au seuil préconisé de 75.00%,"
        " :green[le risque de défaut de paiement est faible.]"
    )
    mock_st.button.assert_called_once_with("Fermer")


def test_render_prediction_modal_disapproved(mock_st, mock_modal):
    mock_modal_class, mock_modal_instance = mock_modal

    translations = {
        "prediction_title": "Score de crédit",
        "probability_score": "Le score de confiance calculé pour ce profil"
        " client est de {probabilite}%.",
        "prediction": "Cela est inférieur au seuil préconisé de {seuil}%, ",
        "credit_approved": "le risque de défaut de paiement est faible.",
        "credit_disapproved": "un risque de défaut de paiement existe.",
        "close_button": "Fermer",
    }
    score_data = {"prediction": False, "probabilite": 0.65, "seuil": 0.75}

    modal = render_prediction_modal(translations, score_data)

    assert modal == mock_modal_instance
    mock_modal_class.assert_called_once_with(key="prediction_modal", title="Score de crédit")
    mock_modal_instance.container.assert_called_once()

    mock_st.write.assert_any_call(
        "Le score de confiance calculé pour ce profil client est de 65.00%."
    )
    mock_st.write.assert_any_call(
        "Cela est inférieur au seuil préconisé de 75.00%,"
        " :red[un risque de défaut de paiement existe.]"
    )
    mock_st.button.assert_called_once_with("Fermer")


def test_render_prediction_modal_close_button(mock_st, mock_modal):
    mock_modal_class, mock_modal_instance = mock_modal

    translations = {
        "prediction_title": "Score de crédit",
        "probability_score": "Le score de confiance calculé pour ce profil"
        " client est de {probabilite}%.",
        "prediction": "Cela est inférieur au seuil préconisé de {seuil}%, ",
        "credit_approved": "le risque de défaut de paiement est faible.",
        "credit_disapproved": "un risque de défaut de paiement existe.",
        "close_button": "Fermer",
    }
    score_data = {"prediction": True, "probabilite": 0.85, "seuil": 0.75}

    mock_st.button.return_value = True
    modal = render_prediction_modal(translations, score_data)

    assert modal == mock_modal_instance
    mock_modal_class.assert_called_once_with(key="prediction_modal", title="Score de crédit")
    mock_modal_instance.container.assert_called_once()

    mock_st.button.assert_called_once_with("Fermer")
    assert mock_st.session_state["show_prediction_modal"] is False
    mock_st.rerun.assert_called_once()
