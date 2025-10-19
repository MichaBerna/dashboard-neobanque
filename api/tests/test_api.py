from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.main_api import app, check_client_trouve, raise_unknown_exception, raise_value_error


# Fixture & mocks
@pytest.fixture
def api():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_model():
    return MagicMock(), 0.5, MagicMock()


# Tests pour check_client_trouve
def test_check_client_trouve_ok(client_fixture):
    assert check_client_trouve(client_fixture) == client_fixture


def test_check_client_trouve_not_found():
    with pytest.raises(HTTPException) as excinfo:
        check_client_trouve(None)
    assert excinfo.value.status_code == 404
    assert "Client non trouvé" in str(excinfo.value.detail)


# Tests pour POST /clients
@patch("api.main_api.create_client")
def test_create_new_client_success(mock_create, client_fixture, client_create_fixture, api):
    mock_create.return_value = client_fixture
    response = api.post(
        "/clients/", json=client_create_fixture.model_dump(), headers={"X-API-Key": "valid_key"}
    )
    assert response.status_code == 200
    assert response.json() == client_fixture.to_response().model_dump()


@patch("api.main_api.create_client")
def test_create_new_client_validation_error(mock_create, api, invalid_client_create_fixture):
    mock_create.side_effect = ValueError("Adresse email invalide")
    response = api.post(
        "/clients/",
        json=invalid_client_create_fixture.model_dump(),
        headers={"X-API-Key": "valid_key"},
    )
    assert response.status_code == 400
    assert "Adresse email invalide" in response.json()["detail"]


# Tests pour GET /clients
@patch("api.main_api.get_clients")
def test_read_clients_success(mock_get, api, client_fixture):
    mock_get.return_value = [client_fixture]
    response = api.get("/clients/", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0] == client_fixture.to_response().model_dump()


# Tests pour GET /clients/{client_id}
@patch("api.main_api.get_client")
def test_read_client_success(mock_get, api, client_fixture):
    mock_get.return_value = client_fixture
    response = api.get("/clients/1", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 200
    assert response.json() == client_fixture.to_response().model_dump()


@patch("api.main_api.get_client")
def test_read_client_not_found(mock_get, api):
    mock_get.return_value = None
    response = api.get("/clients/999", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 404


# Tests pour PUT /clients/{client_id}
@patch("api.main_api.update_client")
def test_update_existing_client_success(mock_update, api, client_create_fixture, client_fixture):
    updated_data = client_create_fixture.model_dump()
    updated_data["nom"] = "Updated"

    # Client modifié
    original_to_response = client_fixture.to_response

    def updated_to_response():
        response = original_to_response()
        response.nom = "Updated"
        return response

    client_fixture.to_response = updated_to_response
    mock_update.return_value = client_fixture

    response = api.put("/clients/1", json=updated_data, headers={"X-API-Key": "valid_key"})
    assert response.status_code == 200
    assert response.json()["nom"] == "Updated"


@patch("api.main_api.update_client")
def test_update_existing_client_validation_error(mock_update, api, invalid_client_create_fixture):
    mock_update.side_effect = ValueError("Adresse email invalide")

    response = api.put(
        "/clients/1",
        json=invalid_client_create_fixture.model_dump(),
        headers={"X-API-Key": "valid_key"},
    )

    assert response.status_code == 400
    assert "Adresse email invalide" in response.json()["detail"]


# Tests pour DELETE /clients/{client_id}
@patch("api.main_api.delete_client")
def test_delete_existing_client_success(mock_delete, api, client_fixture):
    mock_delete.return_value = client_fixture
    response = api.delete("/clients/1", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 200


# Tests pour POST /clients/{client_id}/predict
@patch("api.main_api.db_session")
@patch("api.main_api.model")
@patch("api.main_api.preprocessor")
def test_predict_success(mock_preprocessor, mock_model, mock_db, client_fixture, api):
    mock_db.return_value.query.return_value.filter.return_value.first.return_value = client_fixture
    mock_preprocessor.transform.return_value = [[1, 2, 3]]
    mock_model.predict_proba.return_value = [[0.2, 0.8]]
    response = api.get("/clients/1/predict", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 200
    assert response.json()["prediction"] == 1
    assert response.json()["probabilite"] < 1 and response.json()["probabilite"] > 0
    assert response.json()["seuil"] < 1 and response.json()["seuil"] > 0


@patch("api.main_api.db_session")
def test_predict_client_not_found(mock_db, api):
    mock_db.return_value.query.return_value.filter.return_value.first.return_value = None
    response = api.get("/clients/999/predict", headers={"X-API-Key": "valid_key"})
    assert response.status_code == 404


def test_health_check(api):
    response = api.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_raise_unknown_exception():
    with pytest.raises(HTTPException) as excinfo:
        raise_unknown_exception(Exception("Test error"))
    assert excinfo.value.status_code == 500
    assert "Erreur serveur : Test error" in str(excinfo.value.detail)


def test_raise_value_error():
    with pytest.raises(HTTPException) as excinfo:
        raise_value_error(ValueError("Test value error"))
    assert excinfo.value.status_code == 400
    assert "Test value error" in str(excinfo.value.detail)
