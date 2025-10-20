from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from utils.forms import render_data_field, render_input_field


@pytest.fixture
def mock_st():
    with patch("utils.forms.st") as mock_st:
        yield mock_st


def test_render_input_field_text(mock_st):
    col = MagicMock()
    translations = {"nom": "Nom", "nom_placeholder": "Ex: Berna"}
    client_data = {"nom": "Vador"}
    render_input_field(col, translations, "nom", client_data, "")

    col.__enter__.assert_called_once()
    mock_st.text_input.assert_called_once_with(
        "Nom", value="Vador", placeholder="Ex: Berna", key="nom"
    )


def test_render_input_field_select(mock_st):
    col = MagicMock()
    translations = {"genre": "Genre"}
    client_data = {"genre": "Homme"}
    options = ["Homme", "Femme"]
    render_input_field(col, translations, "genre", client_data, "", "select", options)

    col.__enter__.assert_called_once()
    mock_st.selectbox.assert_called_once_with(
        "Genre", options=["Homme", "Femme"], index=0, key="genre"
    )


def test_render_input_field_date(mock_st):
    col = MagicMock()
    translations = {"date_naissance": "Date de naissance"}
    client_data = {"date_naissance": "1990-01-01"}
    render_input_field(col, translations, "date_naissance", client_data, "", "date")

    col.__enter__.assert_called_once()
    mock_st.date_input.assert_called_once_with(
        "Date de naissance", value=datetime(1990, 1, 1).date(), key="date_naissance"
    )


def test_render_input_field_number(mock_st):
    col = MagicMock()
    translations = {"age": "Age"}
    client_data = {"age": 30}
    render_input_field(col, translations, "age", client_data, 0, "number")

    col.__enter__.assert_called_once()
    mock_st.number_input.assert_called_once_with("Age", value=30, key="age")


def test_render_input_field_default_value(mock_st):
    col = MagicMock()
    translations = {"nom": "Last Name", "nom_placeholder": "Ex: Smith"}
    client_data = {}
    render_input_field(col, translations, "nom", client_data, "Default")

    col.__enter__.assert_called_once()
    mock_st.text_input.assert_called_once_with(
        "Last Name", value="Default", placeholder="Ex: Smith", key="nom"
    )


def test_render_input_field_invalid_date(mock_st):
    col = MagicMock()
    translations = {"date_naissance": "Date de naissance"}
    client_data = {"date_naissance": "invalid-date"}
    render_input_field(col, translations, "date_naissance", client_data, "", "date")

    col.__enter__.assert_called_once()
    mock_st.date_input.assert_called_once_with(
        "Date de naissance", value=None, key="date_naissance"
    )


def test_render_data_field(mock_st):
    col = MagicMock()
    translations = {"nom": "Nom"}
    client_data = {"nom": "Berna"}
    render_data_field(col, translations, "nom", client_data, "")

    col.__enter__.assert_called_once()
    mock_st.markdown.assert_called_once_with("**Nom** : Berna ")


def test_render_data_field_with_suffix(mock_st):
    col = MagicMock()
    translations = {"age": "Age"}
    client_data = {"age": 30}
    render_data_field(col, translations, "age", client_data, "ans")

    col.__enter__.assert_called_once()
    mock_st.markdown.assert_called_once_with("**Age** : 30 ans")
