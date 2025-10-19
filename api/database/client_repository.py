from sqlalchemy.orm import Session

from api.database.models import Client


def get_client(db: Session, client_id: int) -> Client | None:
    return db.query(Client).filter(Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    return db.query(Client).offset(skip).limit(limit).all()


def create_client(db: Session, client_data: dict) -> Client:
    db_client = Client(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, client_data: dict) -> Client | None:
    db_client = get_client(db, client_id)
    if db_client:
        for key, value in client_data.items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int) -> Client | None:
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client
