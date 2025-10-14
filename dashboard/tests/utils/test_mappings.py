from datetime import date, timedelta

import pytest
from utils.mappings import transform_data_for_backend


@pytest.fixture
def base_data():
    return {"nom": "Berna", "prenom": "Micha", "email": "micha.berna@neobanque.com"}


def test_transform_data_for_backend_with_valid_date(base_data):
    today = date.today()
    birth_date = today - timedelta(days=10000)
    data = base_data.copy()
    data["date_naissance"] = birth_date

    transformed = transform_data_for_backend(data)

    assert "DAYS_BIRTH" in transformed
    assert transformed["DAYS_BIRTH"] == -10000
    assert transformed["date_naissance"] == birth_date.strftime("%Y-%m-%d")


def test_transform_data_for_backend_without_birthdate(base_data):
    transformed = transform_data_for_backend(base_data)
    assert transformed == base_data
    assert "DAYS_BIRTH" not in transformed
