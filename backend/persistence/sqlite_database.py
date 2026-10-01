from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..persistence.database import Database
from ..persistence.sqlalchemy_base import SQLAlchemyBase

class SQLiteDatabase(Database):
    DATABASE_URL = "sqlite:///./backend/tickets.db"

    engine = create_engine(DATABASE_URL)

    SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

    def create_tables(self):
        SQLAlchemyBase.metadata.create_all(self.engine)
    