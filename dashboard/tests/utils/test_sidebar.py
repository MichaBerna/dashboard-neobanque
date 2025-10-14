from unittest.mock import MagicMock, patch

import pytest

from dashboard.sidebar import render_language_selector, render_sidebar


@pytest.fixture
def mock_st():
    with patch("dashboard.sidebar.st") as mock_st:
        yield mock_st


@pytest.fixture
def mock_authenticator():
    return MagicMock()


@pytest.fixture
def mock_load_translations():
    with patch("dashboard.sidebar.load_translations") as mock_load:
        mock_load.return_value = {"logout": "Logout"}
        yield mock_load


def test_render_language_selector(mock_st, mock_load_translations):
    mock_st.sidebar.selectbox.return_value = "English"

    translations = render_language_selector()

    mock_st.sidebar.selectbox.assert_called_once_with(
        "Language", ["Français", "English"], key="language_selector", label_visibility="collapsed"
    )
    mock_load_translations.assert_called_once_with("en")
    assert translations == {"logout": "Logout"}


def test_render_sidebar_authenticated(mock_st, mock_authenticator, mock_load_translations):
    mock_st.session_state.get.side_effect = lambda key: {
        "name": "Micha Berna",
        "authentication_status": True,
    }.get(key)
    mock_load_translations.return_value = {"logout": "Logout"}

    translations = render_sidebar(mock_authenticator, authentication_status=True)

    mock_st.sidebar.subheader.assert_called_once_with("Micha Berna", divider="blue")
    mock_authenticator.logout.assert_called_once_with("Logout", "sidebar")
    assert translations == {"logout": "Logout"}


def test_render_sidebar_not_authenticated(mock_st, mock_authenticator, mock_load_translations):
    mock_st.session_state.get.side_effect = lambda key: {"authentication_status": False}.get(key)
    mock_load_translations.return_value = {"logout": "Logout"}

    translations = render_sidebar(mock_authenticator, authentication_status=False)

    mock_st.sidebar.subheader.assert_not_called()
    mock_authenticator.logout.assert_not_called()
    assert translations == {"logout": "Logout"}
