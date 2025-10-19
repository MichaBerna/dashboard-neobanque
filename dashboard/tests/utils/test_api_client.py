from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_env():
    with (
        patch.dict(
            "os.environ",
            {"API_URL": "http://mock-api-url", "STREAMLIT_API_KEY": "mock_api_key"},
            clear=True,
        ),
        patch("dashboard.utils.api_client.load_dotenv"),
    ):
        yield


@pytest.fixture
def mock_requests():
    with patch("dashboard.utils.api_client.requests") as mock_requests:
        yield mock_requests


@pytest.fixture
def mock_st_error():
    with patch("dashboard.utils.api_client.st.error") as mock_st_error:
        yield mock_st_error


def test_get_headers_with_api_key(mock_env):
    from dashboard.utils.api_client import get_headers

    assert get_headers() == {"Authorization": "Bearer mock_api_key"}


# Tests pour create_client
def test_create_client_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import create_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "New Client"}
    mock_requests.post.return_value = mock_response

    data = {"name": "New Client"}
    assert create_client(data) == {"id": 1, "name": "New Client"}
    mock_requests.post.assert_called_once_with(
        "http://mock-api-url/clients/",
        json=data,
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=10,
    )
    mock_st_error.assert_not_called()


def test_create_client_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import create_client

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_requests.post.return_value = mock_response

    data = {"name": "New Client"}
    assert create_client(data) is None
    mock_st_error.assert_called_once_with("Erreur 400 : Bad Request")


def test_create_client_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import create_client

    mock_requests.post.side_effect = Exception("Timeout error")

    data = {"name": "New Client"}
    assert create_client(data) is None
    mock_st_error.assert_called_once_with("Erreur lors de la création du client : Timeout error")


# Tests pour update_client
def test_update_client_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import update_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Updated Client"}
    mock_requests.put.return_value = mock_response

    data = {"name": "Updated Client"}
    assert update_client(1, data) == {"id": 1, "name": "Updated Client"}
    mock_requests.put.assert_called_once_with(
        "http://mock-api-url/clients/1",
        json=data,
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=10,
    )
    mock_st_error.assert_not_called()


def test_update_client_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import update_client

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_requests.put.return_value = mock_response

    data = {"name": "Updated Client"}
    assert update_client(1, data) is None
    mock_st_error.assert_called_once_with("Erreur 404 : Not Found")


def test_update_client_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import update_client

    mock_requests.put.side_effect = Exception("Timeout error")

    data = {"name": "Updated Client"}
    assert update_client(1, data) is None
    mock_st_error.assert_called_once_with("Erreur lors de la mise à jour du client : Timeout error")


# Tests pour delete_client
def test_delete_client_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import delete_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_requests.delete.return_value = mock_response

    delete_client(1)
    mock_requests.delete.assert_called_once_with(
        "http://mock-api-url/clients/1",
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=10,
    )
    mock_st_error.assert_not_called()


def test_delete_client_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import delete_client

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_requests.delete.return_value = mock_response

    delete_client(1)
    mock_st_error.assert_called_once_with("Erreur 404 : Not Found")


def test_delete_client_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import delete_client

    mock_requests.delete.side_effect = Exception("Timeout error")

    delete_client(1)
    mock_st_error.assert_called_once_with("Erreur lors de la suppression du client : Timeout error")


# Tests pour get_clients
def test_get_clients_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_clients

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Client 1"}]
    mock_requests.get.return_value = mock_response

    assert get_clients() == [{"id": 1, "name": "Client 1"}]
    mock_requests.get.assert_called_once_with(
        "http://mock-api-url/clients/",
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=10,
    )
    mock_st_error.assert_not_called()


def test_get_clients_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_clients

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_requests.get.return_value = mock_response

    assert get_clients() == []
    mock_st_error.assert_called_once_with("Erreur 500 : Internal Server Error")


def test_get_clients_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_clients

    mock_requests.get.side_effect = Exception("Timeout error")

    assert get_clients() == []
    mock_st_error.assert_called_once_with(
        "Erreur lors de la récupération des clients : Timeout error"
    )


# Tests pour get_client
def test_get_client_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Client 1"}
    mock_requests.get.return_value = mock_response

    assert get_client(1) == {"id": 1, "name": "Client 1"}
    mock_requests.get.assert_called_once_with(
        "http://mock-api-url/clients/1",
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=10,
    )
    mock_st_error.assert_not_called()


def test_get_client_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_client

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_requests.get.return_value = mock_response

    assert get_client(999) is None
    mock_st_error.assert_called_once_with("Erreur 404 : Not Found")


def test_get_client_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import get_client

    mock_requests.get.side_effect = Exception("Timeout error")

    assert get_client(1) is None
    mock_st_error.assert_called_once_with(
        "Erreur lors de la récupération du client : Timeout error"
    )


# Tests pour call_predict_api
def test_call_predict_api_success(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import call_predict_api

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"prediction": 0.95}
    mock_requests.get.return_value = mock_response

    assert call_predict_api(1) == {"prediction": 0.95}
    mock_requests.get.assert_called_once_with(
        "http://mock-api-url/clients/1/predict",
        headers={"Authorization": "Bearer mock_api_key"},
        timeout=20,
    )
    mock_st_error.assert_not_called()


def test_call_predict_api_failure(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import call_predict_api

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_requests.get.return_value = mock_response

    assert call_predict_api(1) is None
    mock_st_error.assert_called_once_with("Erreur 404 : Not Found")


def test_call_predict_api_exception(mock_env, mock_requests, mock_st_error):
    from dashboard.utils.api_client import call_predict_api

    mock_requests.get.side_effect = Exception("Timeout error")

    assert call_predict_api(1) is None
    mock_st_error.assert_called_once_with("Erreur lors de l'appel à l'API : Timeout error")
