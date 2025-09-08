from datetime import date
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.database.models import Client
from api.dto.client_dto import ClientCreate, ClientResponse
from api.main import app


@pytest.fixture
def client_fixture(client_response_fixture):
    client_fixture = Client(
        id=1,
        nom="Doe",
        prenom="John",
        date_naissance=date(1990, 1, 1),
        adresse="123 Rue Test",
        telephone="+33612345678",
        email="john.doe@example.com",
        CODE_GENDER="M",
        NAME_INCOME_TYPE="Salarié",
        NAME_EDUCATION_TYPE="Supérieur",
        NAME_HOUSING_TYPE="Propriétaire",
        DAYS_BIRTH=-11603,
        DAYS_EMPLOYED=-1000,
        DAYS_REGISTRATION=-500,
        DAYS_ID_PUBLISH=-300,
        FLAG_EMP_PHONE=False,
        REGION_RATING_CLIENT=1,
        REG_CITY_NOT_LIVE_CITY=False,
        REG_CITY_NOT_WORK_CITY=False,
        EXT_SOURCE_1=0.5,
        EXT_SOURCE_2=0.5,
        EXT_SOURCE_3=0.5,
        YEARS_BEGINEXPLUATATION_AVG=10.0,
        YEARS_BUILD_AVG=20.0,
        ELEVATORS_AVG=1.0,
        ENTRANCES_AVG=2.0,
        FLOORSMAX_AVG=5.0,
        FLOORSMIN_AVG=1.0,
        HOUSETYPE_MODE="Appartement",
        WALLSMATERIAL_MODE="Brique",
        EMERGENCYSTATE_MODE="Non",
        DAYS_LAST_PHONE_CHANGE=-100,
        FLAG_DOCUMENT_3=False,
    )
    client_fixture.to_response = lambda: client_response_fixture
    return client_fixture


@pytest.fixture
def client_create_fixture():
    return ClientCreate(
        nom="Doe",
        prenom="John",
        date_naissance="1990-01-01",
        adresse="123 Rue Test",
        telephone="+33612345678",
        email="john.doe@example.com",
        CODE_GENDER="M",
        NAME_INCOME_TYPE="Salarié",
        NAME_EDUCATION_TYPE="Supérieur",
        NAME_HOUSING_TYPE="Propriétaire",
        DAYS_BIRTH=-11603,
        DAYS_EMPLOYED=-1000,
        DAYS_REGISTRATION=-500,
        DAYS_ID_PUBLISH=-300,
        FLAG_EMP_PHONE=False,
        REGION_RATING_CLIENT=1,
        REG_CITY_NOT_LIVE_CITY=False,
        REG_CITY_NOT_WORK_CITY=False,
        EXT_SOURCE_1=0.5,
        EXT_SOURCE_2=0.5,
        EXT_SOURCE_3=0.5,
        YEARS_BEGINEXPLUATATION_AVG=10.0,
        YEARS_BUILD_AVG=20.0,
        ELEVATORS_AVG=1.0,
        ENTRANCES_AVG=2.0,
        FLOORSMAX_AVG=5.0,
        FLOORSMIN_AVG=1.0,
        HOUSETYPE_MODE="Appartement",
        WALLSMATERIAL_MODE="Brique",
        EMERGENCYSTATE_MODE="Non",
        DAYS_LAST_PHONE_CHANGE=-100,
        FLAG_DOCUMENT_3=False,
    )


@pytest.fixture
def invalid_client_create_fixture():
    return ClientCreate(
        nom="Doe",
        prenom="John",
        date_naissance="1990-01-01",
        adresse="123 Rue Test",
        telephone="+33612345678",
        email="invalid-email",  # Email invalide
        CODE_GENDER="M",
        NAME_INCOME_TYPE="Salarié",
        NAME_EDUCATION_TYPE="Supérieur",
        NAME_HOUSING_TYPE="Propriétaire",
        DAYS_BIRTH=-11603,
        DAYS_EMPLOYED=-1000,
        DAYS_REGISTRATION=-500,
        DAYS_ID_PUBLISH=-300,
        FLAG_EMP_PHONE=False,
        REGION_RATING_CLIENT=1,
        REG_CITY_NOT_LIVE_CITY=False,
        REG_CITY_NOT_WORK_CITY=False,
        EXT_SOURCE_1=0.5,
        EXT_SOURCE_2=0.5,
        EXT_SOURCE_3=0.5,
        YEARS_BEGINEXPLUATATION_AVG=10.0,
        YEARS_BUILD_AVG=20.0,
        ELEVATORS_AVG=1.0,
        ENTRANCES_AVG=2.0,
        FLOORSMAX_AVG=5.0,
        FLOORSMIN_AVG=1.0,
        HOUSETYPE_MODE="Appartement",
        WALLSMATERIAL_MODE="Brique",
        EMERGENCYSTATE_MODE="Non",
        DAYS_LAST_PHONE_CHANGE=-100,
        FLAG_DOCUMENT_3=False,
    )


@pytest.fixture
def client_response_fixture():
    return ClientResponse(
        id=1,
        nom="Doe",
        prenom="John",
        age=35,
        date_naissance="1990-01-01",
        adresse="123 Rue Test",
        telephone="+33612345678",
        email="invalid-email",  # Email invalide
        CODE_GENDER="M",
        NAME_INCOME_TYPE="Salarié",
        NAME_EDUCATION_TYPE="Supérieur",
        NAME_HOUSING_TYPE="Propriétaire",
        DAYS_BIRTH=-11603,
        DAYS_EMPLOYED=-1000,
        DAYS_REGISTRATION=-500,
        DAYS_ID_PUBLISH=-300,
        FLAG_EMP_PHONE=False,
        REGION_RATING_CLIENT=1,
        REG_CITY_NOT_LIVE_CITY=False,
        REG_CITY_NOT_WORK_CITY=False,
        EXT_SOURCE_1=0.5,
        EXT_SOURCE_2=0.5,
        EXT_SOURCE_3=0.5,
        YEARS_BEGINEXPLUATATION_AVG=10.0,
        YEARS_BUILD_AVG=20.0,
        ELEVATORS_AVG=1.0,
        ENTRANCES_AVG=2.0,
        FLOORSMAX_AVG=5.0,
        FLOORSMIN_AVG=1.0,
        HOUSETYPE_MODE="Appartement",
        WALLSMATERIAL_MODE="Brique",
        EMERGENCYSTATE_MODE="Non",
        DAYS_LAST_PHONE_CHANGE=-100,
        FLAG_DOCUMENT_3=False,
    )


@pytest.fixture
def api():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_env_valid_keys():
    with patch.dict("os.environ", {"VALID_API_KEYS": "valid_key1,valid_key2"}):
        yield
