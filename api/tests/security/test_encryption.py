import importlib
import os
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet, InvalidToken

from api.security.encryption import decrypt, encrypt

VALID_KEY = Fernet.generate_key().decode()


@patch.dict(os.environ, {"DB_ENCRYPTION_KEY": VALID_KEY})
def test_key_from_environment():
    import api.security.encryption

    importlib.reload(api.security.encryption)

    assert api.security.encryption.KEY == VALID_KEY


@patch.dict(os.environ, {}, clear=True)
def test_key_generation():
    import api.security.encryption

    importlib.reload(api.security.encryption)

    assert len(api.security.encryption.KEY) == 44


@patch.dict(os.environ, {"DB_ENCRYPTION_KEY": Fernet.generate_key().decode()})
def test_encrypt_decrypt():
    original_data = "Données sensibles à chiffrer"
    encrypted_data = encrypt(original_data)
    decrypted_data = decrypt(encrypted_data)

    assert encrypted_data != original_data
    assert decrypted_data == original_data


@patch.dict(os.environ, {"DB_ENCRYPTION_KEY": Fernet.generate_key().decode()})
def test_decrypt_invalid_key():
    original_data = "Données sensibles à chiffrer"
    encrypted_data = encrypt(original_data)

    with patch.dict(os.environ, {"DB_ENCRYPTION_KEY": Fernet.generate_key().decode()}):
        import api.security.encryption

        importlib.reload(api.security.encryption)

        with pytest.raises(InvalidToken):
            decrypt(encrypted_data)
