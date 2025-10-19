from typing import Annotated

from api_key_auth import get_api_key
from database.client_repository import (
    create_client,
    delete_client,
    get_client,
    get_clients,
    update_client,
)
from database.database_init import db_session, init_db
from dto.prediction_response import PredictionResponse
from fastapi import Depends, FastAPI, HTTPException
from model.client_model import client_to_model_input
from model.model_loader import load_model
from sqlalchemy.orm import Session

from api.database.models import Client
from api.dto.client_dto import ClientCreate, ClientResponse

# Initialisation BDD/Session
init_db()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]

# Initialisation API et modèle IA
app = FastAPI()
model, seuil, preprocessor = load_model()


@app.post("/clients/", response_model=ClientResponse)
def create_new_client(db: DbSession, client: ClientCreate, api_key: str = Depends(get_api_key)):
    try:
        db_client = create_client(db, client.model_dump())
        return db_client.to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur : " + str(e)) from e


@app.get("/clients/", response_model=list[ClientResponse])
def read_clients(
    db: DbSession, skip: int = 0, limit: int = 100, api_key: str = Depends(get_api_key)
):
    clients = get_clients(db, skip, limit)
    return [client.to_response() for client in clients]


@app.get("/clients/{client_id}", response_model=ClientResponse)
def read_client(db: DbSession, client_id: int, api_key: str = Depends(get_api_key)):
    db_client = get_client(db, client_id)
    return check_client_trouve(db_client).to_response()


@app.put("/clients/{client_id}", response_model=ClientResponse)
def update_existing_client(
    db: DbSession, client_id: int, client: ClientCreate, api_key: str = Depends(get_api_key)
):
    try:
        db_client = update_client(db, client_id, client.model_dump())
        return check_client_trouve(db_client).to_response()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur : " + str(e)) from e


@app.delete("/clients/{client_id}")
def delete_existing_client(db: DbSession, client_id: int, api_key: str = Depends(get_api_key)):
    delete_client(db, client_id)


@app.get("/clients/{client_id}/predict", response_model=PredictionResponse)
async def predict(db: DbSession, client_id: int, api_key: str = Depends(get_api_key)):
    client = db.query(Client).filter(Client.id == client_id).first()
    check_client_trouve(client)
    model_input = client_to_model_input(client)

    try:
        input_data_processed = preprocessor.transform(model_input)
        probabilite = model.predict_proba(input_data_processed)[0][1]
        prediction = probabilite >= seuil
        return PredictionResponse(prediction=prediction, probabilite=probabilite, seuil=seuil)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur : " + str(e)) from e


@app.get("/health")
async def health_check():
    return {"status": "ok"}


def check_client_trouve(client):
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client
