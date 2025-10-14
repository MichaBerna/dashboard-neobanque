from unittest.mock import patch

import pytest
from utils.rgpd import show_rgpd_conseiller


@pytest.fixture
def mock_translations():
    return {
        "rgpd_conseiller_title": "Consentement RGPD",
        "rgpd_conseiller_intro": "En tant que conseiller bancaire, vous devez accepter les...",
        "rgpd_conseiller_details_label": "Détails des engagements",
        "rgpd_conseiller_detail_1": "- Respecter la confidentialité des données clients",
        "rgpd_conseiller_detail_2": "- N'utiliser les données qu'à des fins professionnelles...",
        "rgpd_conseiller_detail_3": "- Ne pas partager les données en dehors du cadre légal",
        "rgpd_conseiller_checkbox": "J'accepte les conditions d'utilisation des données clients",
        "rgpd_conseiller_success": "Conditions d'utilisation des données acceptées",
        "rgpd_conseiller_warning": "Vous devez accepter pour continuer",
    }


@pytest.fixture
def mock_st():
    with patch("utils.rgpd.st") as mock_st:
        yield mock_st


def test_show_rgpd_conseiller_display(mock_st, mock_translations):
    show_rgpd_conseiller(mock_translations)

    mock_st.container.assert_called_once()
    mock_st.subheader.assert_called_once_with(mock_translations["rgpd_conseiller_title"])
    mock_st.write.assert_any_call(mock_translations["rgpd_conseiller_intro"])
    mock_st.write.assert_any_call(mock_translations["rgpd_conseiller_detail_1"])
    mock_st.write.assert_any_call(mock_translations["rgpd_conseiller_detail_2"])
    mock_st.write.assert_any_call(mock_translations["rgpd_conseiller_detail_3"])
    mock_st.checkbox.assert_called_once_with(mock_translations["rgpd_conseiller_checkbox"])


def test_show_rgpd_conseiller_checkbox_checked(mock_st, mock_translations):
    mock_st.checkbox.return_value = True

    show_rgpd_conseiller(mock_translations)
    mock_st.success.assert_called_once_with(mock_translations["rgpd_conseiller_success"])


def test_show_rgpd_conseiller_checkbox_unchecked(mock_st, mock_translations):
    mock_st.checkbox.return_value = False

    show_rgpd_conseiller(mock_translations)
    mock_st.error.assert_called_once_with(mock_translations["rgpd_conseiller_warning"])
