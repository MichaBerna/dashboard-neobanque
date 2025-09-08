from datetime import date

from api.database.client_repository import (
    create_client,
    delete_client,
    get_client,
    get_clients,
    update_client,
)


def test_get_client_found(mock_db_session, client_fixture):
    mock_db_session.query.return_value.filter.return_value.first.return_value = client_fixture

    result = get_client(mock_db_session, 1)

    assert result == client_fixture
    mock_db_session.query.assert_called_once()


def test_get_client_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = get_client(mock_db_session, 999)

    assert result is None
    mock_db_session.query.assert_called_once()


def test_get_clients(mock_db_session, client_fixture):
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        client_fixture
    ]

    result = get_clients(mock_db_session, skip=0, limit=100)

    assert result == [client_fixture]
    mock_db_session.query.assert_called_once()


def test_get_clients_empty(mock_db_session):
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []

    result = get_clients(mock_db_session, skip=0, limit=100)

    assert result == []
    mock_db_session.query.assert_called_once()


def test_create_client_success(mock_db_session):
    client_data = {
        "id": 1,
        "nom": "Doe",
        "prenom": "John",
        "date_naissance": date(1990, 1, 1),
        "adresse": "123 Rue Test",
        "telephone": "+33612345678",
        "email": "john.doe@example.com",
        "CODE_GENDER": "M",
        "NAME_INCOME_TYPE": "Salarié",
        "NAME_EDUCATION_TYPE": "Supérieur",
        "NAME_HOUSING_TYPE": "Propriétaire",
        "DAYS_BIRTH": -11603,
        "DAYS_EMPLOYED": -1000,
        "DAYS_REGISTRATION": -500,
        "DAYS_ID_PUBLISH": -300,
        "FLAG_EMP_PHONE": False,
        "REGION_RATING_CLIENT": 1,
        "REG_CITY_NOT_LIVE_CITY": False,
        "REG_CITY_NOT_WORK_CITY": False,
        "EXT_SOURCE_1": 0.5,
        "EXT_SOURCE_2": 0.5,
        "EXT_SOURCE_3": 0.5,
        "YEARS_BEGINEXPLUATATION_AVG": 10.0,
        "YEARS_BUILD_AVG": 20.0,
        "ELEVATORS_AVG": 1.0,
        "ENTRANCES_AVG": 2.0,
        "FLOORSMAX_AVG": 5.0,
        "FLOORSMIN_AVG": 1.0,
        "HOUSETYPE_MODE": "Appartement",
        "WALLSMATERIAL_MODE": "Brique",
        "EMERGENCYSTATE_MODE": "Non",
        "DAYS_LAST_PHONE_CHANGE": -100,
        "FLAG_DOCUMENT_3": False,
    }

    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = create_client(mock_db_session, client_data)

    assert result == mock_db_session.add.call_args[0][0]
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


def test_update_client_success(mock_db_session, client_fixture):
    client_data = {"nom": "Updated"}

    mock_db_session.query.return_value.filter.return_value.first.return_value = client_fixture
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    result = update_client(mock_db_session, 1, client_data)

    assert result == client_fixture
    client_fixture.nom = "Updated"
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


def test_update_client_not_found(mock_db_session):
    client_data = {"nom": "Updated"}

    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = update_client(mock_db_session, 999, client_data)

    assert result is None
    mock_db_session.commit.assert_not_called()


def test_delete_client_success(mock_db_session, client_fixture):
    mock_db_session.query.return_value.filter.return_value.first.return_value = client_fixture
    mock_db_session.delete.return_value = None
    mock_db_session.commit.return_value = None

    result = delete_client(mock_db_session, 1)

    assert result == client_fixture
    mock_db_session.delete.assert_called_once_with(client_fixture)
    mock_db_session.commit.assert_called_once()


def test_delete_client_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = delete_client(mock_db_session, 999)

    assert result is None
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()
