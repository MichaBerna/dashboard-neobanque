import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key_header = APIKeyHeader(name="Authorization", scheme_name="Bearer", auto_error=False)
VALID_API_KEYS = os.getenv("VALID_API_KEYS", "").split(",") if os.getenv("VALID_API_KEYS") else []


def get_api_key(api_key: str = Security(api_key_header)):
    # Enlever "Bearer "
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[7:]

    # Clé non requise (mode local)
    if not VALID_API_KEYS:
        logger.warning(
            "Aucune clé API requise (mode local). Si déployé, veillez à configurer VALID_API_KEYS"
        )
        return api_key

    # Clé requise mais non fournie
    if not api_key:
        logger.error("Clé API manquante")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clé API manquante")

    # Clé fournie mais invalide
    if api_key not in VALID_API_KEYS:
        logger.error(f"Clé API invalide : '{api_key}'.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clé API invalide")

    return api_key
