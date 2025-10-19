from unittest import mock

import dashboard.config as config


def test_set_page_config():
    mock_st = mock.Mock()
    with mock.patch("dashboard.config.st", mock_st):
        config.set_page_config()

    mock_st.set_page_config.assert_called_once_with(page_title="Dashboard Neobanque", layout="wide")
    mock_st.markdown.assert_called_once()
