from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database.models import Base

engine = create_engine(
    "sqlite:///./neobanque.db", connect_args={"check_same_thread": False}, echo=True
)

db_session = sessionmaker(engine)


def init_db():
    Base.metadata.create_all(engine)
