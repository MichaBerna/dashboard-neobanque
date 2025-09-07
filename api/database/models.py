from datetime import date
from typing import Any

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from api.security.encryption import decrypt, encrypt

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    # Identifiant unique
    id = Column(Integer, primary_key=True, index=True)

    # Informations personnelles chiffrées
    nom_encrypted = Column("nom", String(500))
    prenom_encrypted = Column("prenom", String(500))
    date_naissance_encrypted = Column("date_naissance", String(50))
    adresse_encrypted = Column("adresse", String(500))
    telephone_encrypted = Column("telephone", String(50))
    email_encrypted = Column("email", String(500))

    # Champs pour la prédiction
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

    @property
    def nom(self) -> str:
        return self.decrypt_str("nom_encrypted")

    @nom.setter
    def nom(self, value: str):
        self.nom_encrypted = encrypt(value)

    @property
    def prenom(self) -> str:
        return self.decrypt_str("prenom_encrypted")

    @prenom.setter
    def prenom(self, value: str):
        self.prenom_encrypted = encrypt(value)

    @property
    def date_naissance(self) -> date:
        return self.decrypt_date("date_naissance_encrypted")

    @date_naissance.setter
    def date_naissance(self, value: date):
        self.date_naissance_encrypted = encrypt(value.isoformat())

    @property
    def adresse(self) -> str:
        return self.decrypt_str("adresse_encrypted")

    @adresse.setter
    def adresse(self, value: str):
        self.adresse_encrypted = encrypt(value)

    @property
    def telephone(self) -> str:
        return self.decrypt_str("telephone_encrypted")

    @telephone.setter
    def telephone(self, value: str):
        self.telephone_encrypted = encrypt(value)

    @property
    def email(self) -> str:
        return self.decrypt_str("email_encrypted")

    @email.setter
    def email(self, value: str):
        self.email_encrypted = encrypt(value)

    @property
    def age(self) -> int:
        return date.today().year - self.date_naissance.year

    def to_response(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance.isoformat(),
            "age": self.age,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "email": self.email,
            "CODE_GENDER": self.CODE_GENDER,
            "NAME_INCOME_TYPE": self.NAME_INCOME_TYPE,
            "NAME_EDUCATION_TYPE": self.NAME_EDUCATION_TYPE,
            "NAME_HOUSING_TYPE": self.NAME_HOUSING_TYPE,
            "DAYS_BIRTH": self.DAYS_BIRTH,
            "DAYS_EMPLOYED": self.DAYS_EMPLOYED,
            "DAYS_REGISTRATION": self.DAYS_REGISTRATION,
            "DAYS_ID_PUBLISH": self.DAYS_ID_PUBLISH,
            "FLAG_EMP_PHONE": self.FLAG_EMP_PHONE,
            "REGION_RATING_CLIENT": self.REGION_RATING_CLIENT,
            "REG_CITY_NOT_LIVE_CITY": self.REG_CITY_NOT_LIVE_CITY,
            "REG_CITY_NOT_WORK_CITY": self.REG_CITY_NOT_WORK_CITY,
            "EXT_SOURCE_1": self.EXT_SOURCE_1,
            "EXT_SOURCE_2": self.EXT_SOURCE_2,
            "EXT_SOURCE_3": self.EXT_SOURCE_3,
            "YEARS_BEGINEXPLUATATION_AVG": self.YEARS_BEGINEXPLUATATION_AVG,
            "YEARS_BUILD_AVG": self.YEARS_BUILD_AVG,
            "ELEVATORS_AVG": self.ELEVATORS_AVG,
            "ENTRANCES_AVG": self.ENTRANCES_AVG,
            "FLOORSMAX_AVG": self.FLOORSMAX_AVG,
            "FLOORSMIN_AVG": self.FLOORSMIN_AVG,
            "HOUSETYPE_MODE": self.HOUSETYPE_MODE,
            "WALLSMATERIAL_MODE": self.WALLSMATERIAL_MODE,
            "EMERGENCYSTATE_MODE": self.EMERGENCYSTATE_MODE,
            "DAYS_LAST_PHONE_CHANGE": self.DAYS_LAST_PHONE_CHANGE,
            "FLAG_DOCUMENT_3": self.FLAG_DOCUMENT_3,
        }

    def decrypt_str(self, column_name: str) -> str:
        encrypted_value = getattr(self, column_name)
        return decrypt(encrypted_value)

    def decrypt_date(self, column_name: str) -> date:
        encrypted_value = getattr(self, column_name)
        return date.fromisoformat(decrypt(encrypted_value))
