from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    # Identifiant unique
    id = Column(Integer, primary_key=True, index=True)

    # Informations personnelles
    nom = Column(String(50))
    prenom = Column(String(50))
    date_naissance = Column(Date)
    adresse = Column(String(200))
    telephone = Column(String(20))
    email = Column(String(100))

    # Champs pour la prédiction (mapping avec ClientData)
    CODE_GENDER = Column(String(1))
    NAME_INCOME_TYPE = Column(String(50))
    NAME_EDUCATION_TYPE = Column(String(50))
    NAME_HOUSING_TYPE = Column(String(50))
    DAYS_BIRTH = Column(Float)
    DAYS_EMPLOYED = Column(Float)
    DAYS_REGISTRATION = Column(Float)
    DAYS_ID_PUBLISH = Column(Float)
    FLAG_EMP_PHONE = Column(Integer)
    REGION_RATING_CLIENT = Column(Integer)
    REG_CITY_NOT_LIVE_CITY = Column(Integer)
    REG_CITY_NOT_WORK_CITY = Column(Integer)
    EXT_SOURCE_1 = Column(Float)
    EXT_SOURCE_2 = Column(Float)
    EXT_SOURCE_3 = Column(Float)
    YEARS_BEGINEXPLUATATION_AVG = Column(Float)
    YEARS_BUILD_AVG = Column(Float)
    ELEVATORS_AVG = Column(Float)
    ENTRANCES_AVG = Column(Float)
    FLOORSMAX_AVG = Column(Float)
    FLOORSMIN_AVG = Column(Float)
    HOUSETYPE_MODE = Column(String(50))
    WALLSMATERIAL_MODE = Column(String(50))
    EMERGENCYSTATE_MODE = Column(String(50))
    DAYS_LAST_PHONE_CHANGE = Column(Float)
    FLAG_DOCUMENT_3 = Column(Integer)
