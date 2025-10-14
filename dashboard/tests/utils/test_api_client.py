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
        patch("utils.api_client.load_dotenv"),
    ):
        yield


@pytest.fixture
def mock_requests():
    with patch("utils.api_client.requests") as mock_requests:
        yield mock_requests


@pytest.fixture
def mock_st_error():
    with patch("utils.api_client.st.error") as mock_st_error:
        yield mock_st_error


def test_get_headers_with_api_key(mock_env):
    from utils.api_client import get_headers

    assert get_headers() == {"Authorization": "Bearer mock_api_key"}


def test_get_clients_success(mock_env, mock_requests, mock_st_error):
    from utils.api_client import get_clients

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


def test_get_clients_http_error(mock_env, mock_requests, mock_st_error):
    from utils.api_client import get_clients

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_requests.get.return_value = mock_response

    assert get_clients() == []
    mock_st_error.assert_called_once_with("Erreur 500 : Internal Server Error")


def test_get_clients_exception(mock_env, mock_requests, mock_st_error):
    from utils.api_client import get_clients

    mock_requests.get.side_effect = Exception("Connection error")

    assert get_clients() == []
    mock_st_error.assert_called_once_with(
        "Erreur lors de la récupération des clients : Connection error"
    )


# Test pour get_client
def test_get_client_success(mock_env, mock_requests, mock_st_error):
    from utils.api_client import get_client

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


# Test pour call_predict_api
def test_call_predict_api_success(mock_env, mock_requests, mock_st_error):
    from utils.api_client import call_predict_api

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
