from pydantic import BaseModel

from api.database.models import Client


class ClientModel(BaseModel):
    CODE_GENDER: str
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    NAME_HOUSING_TYPE: str
    DAYS_BIRTH: float
    DAYS_EMPLOYED: float
    DAYS_REGISTRATION: float
    DAYS_ID_PUBLISH: float
    FLAG_EMP_PHONE: int
    REGION_RATING_CLIENT: int
    REG_CITY_NOT_LIVE_CITY: int
    REG_CITY_NOT_WORK_CITY: int
    EXT_SOURCE_1: float
    EXT_SOURCE_2: float
    EXT_SOURCE_3: float
    YEARS_BEGINEXPLUATATION_AVG: float
    YEARS_BUILD_AVG: float
    ELEVATORS_AVG: float
    ENTRANCES_AVG: float
    FLOORSMAX_AVG: float
    FLOORSMIN_AVG: float
    HOUSETYPE_MODE: str
    WALLSMATERIAL_MODE: str
    EMERGENCYSTATE_MODE: str
    DAYS_LAST_PHONE_CHANGE: float
    FLAG_DOCUMENT_3: int


def client_to_client_model(client: Client) -> ClientModel:
    # Récupère les attributs de l'instance SQLAlchemy
    client_data = {}
    for column in client.__table__.columns:
        value = getattr(client, column.name)
        # Convertit les valeurs en types natifs (str, float, int)
        if isinstance(value, str):
            client_data[column.name] = value
        elif isinstance(value, (int, float)):
            client_data[column.name] = float(value) if isinstance(value, float) else int(value)
        else:
            client_data[column.name] = value

    return ClientModel(**client_data)
