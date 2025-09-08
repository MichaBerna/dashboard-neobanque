from unittest.mock import patch

import pytest
from fastapi import HTTPException

from api.api_key_auth import get_api_key


def test_get_api_key_no_validation_required():
    with patch.dict("os.environ", {"VALID_API_KEYS": ""}):
        api_key = get_api_key("any_key")
        assert api_key == "any_key"


def test_get_api_key_missing():
    with patch("api.api_key_auth.VALID_API_KEYS", ["valid_key1", "valid_key2"]):
        with pytest.raises(HTTPException) as excinfo:
            get_api_key("")  # Pas de clé fournie
        assert excinfo.value.status_code == 401
        assert "Clé API manquante" in excinfo.value.detail


def test_get_api_key_invalid():
    with patch("api.api_key_auth.VALID_API_KEYS", ["valid_key1", "valid_key2"]):
        with pytest.raises(HTTPException) as excinfo:
            get_api_key("invalid_key")  # Clé invalide
        assert excinfo.value.status_code == 401
        assert "Clé API invalide" in excinfo.value.detail


def test_get_api_key_valid():
    with patch("api.api_key_auth.VALID_API_KEYS", ["valid_key1", "valid_key2"]):
        api_key = get_api_key("valid_key1")  # Clé valide
        assert api_key == "valid_key1"
