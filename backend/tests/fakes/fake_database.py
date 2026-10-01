from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.persistence.database import Database
from backend.persistence.sqlalchemy_base import SQLAlchemyBase


class FakeDatabase(Database):
    def __init__(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        SQLAlchemyBase.metadata.create_all(self.engine)
