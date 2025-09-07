import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("DB_ENCRYPTION_KEY")
if not KEY:
    KEY = Fernet.generate_key().decode()
    print(f"Nouvelle clé générée : {KEY}")

cipher = Fernet(KEY.encode())


def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


def decrypt(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()
