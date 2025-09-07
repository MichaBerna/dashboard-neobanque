# schemas.py
from datetime import date

from pydantic import BaseModel


class ClientBase(BaseModel):
    nom: str
    prenom: str
    date_naissance: date
    adresse: str
    telephone: str
    email: str
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


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True
