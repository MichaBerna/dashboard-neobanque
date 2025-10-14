import json
from unittest.mock import mock_open, patch

import pytest
from utils.translations import load_translations


def test_load_translations_success():
    mock_json_data = {"key1": "valeur1", "key2": "valeur2"}

    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_json_data))),
        patch("os.path.dirname") as mock_dirname,
        patch("os.path.abspath") as mock_abspath,
        patch("os.path.join") as mock_join,
    ):
        mock_dirname.return_value = "/mock"
        mock_abspath.return_value = "/mock/absolu"
        mock_join.return_value = "/mock/absolu/locales/fr.json"

        result = load_translations("fr")

        assert result == mock_json_data
        mock_join.assert_called_once_with("/mock", "locales", "fr.json")


def test_load_translations_file_not_found():
    with (
        patch("builtins.open", side_effect=FileNotFoundError("Fichier introuvable")),
        patch("os.path.join", return_value="/mock/locales/fr.json"),
        pytest.raises(FileNotFoundError) as excinfo,
    ):
        load_translations("fr")
    assert "Fichier introuvable" in str(excinfo.value)
