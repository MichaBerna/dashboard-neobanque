from datetime import date, timedelta

import pytest

from api.database.models import Client


def test_prenom_validation():
    with pytest.raises(ValueError, match="ne peut pas être vide"):
        Client(prenom="")

    client = Client(prenom=" Jean ")
    assert client.prenom == "Jean"


def test_nom_validation():
    with pytest.raises(ValueError, match="ne peut pas être vide"):
        Client(nom="")

    client = Client(nom=" Dupont ")
    assert client.nom == "Dupont"


def test_telephone_validation():
    with pytest.raises(ValueError, match="ne peut pas être vide"):
        Client(telephone="")

    with pytest.raises(ValueError, match="Numéro de téléphone invalide"):
        Client(telephone="123aze")

    valid_phones = ["0123456789", "+33123456789"]
    for phone in valid_phones:
        client = Client(telephone=phone)
        assert client.telephone == phone


def test_email_validation():
    with pytest.raises(ValueError, match="ne peut pas être vide"):
        Client(email="")

    with pytest.raises(ValueError, match="Adresse email invalide"):
        Client(email="EmailInvalide")

    client = Client(email="test@example.com")
    assert client.email == "test@example.com"


def test_date_naissance_validation():
    future_date = date.today() + timedelta(days=1)
    with pytest.raises(ValueError, match="ne peut pas être dans le futur"):
        Client(date_naissance=future_date)


def test_adresse_validation():
    with pytest.raises(ValueError, match="ne peut pas être vide"):
        Client(adresse="")

    client = Client(adresse=" 123 Rue Principale ")
    assert client.adresse == "123 Rue Principale"
