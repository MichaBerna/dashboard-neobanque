import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

load_dotenv()

api_key_header = APIKeyHeader(name="Authorization", scheme_name="Bearer", auto_error=False)
VALID_API_KEYS = os.getenv("VALID_API_KEYS", "").split(",") if os.getenv("VALID_API_KEYS") else []


def get_api_key(api_key: str = Security(api_key_header)):
    # Clé non requise (pas de VALID_API_KEYS, local)
    if not VALID_API_KEYS:
        return api_key

    # Clé requise mais non fournie
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clé API manquante")

    # Clé fournie mais invalide
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clé API invalide")

    return api_key
