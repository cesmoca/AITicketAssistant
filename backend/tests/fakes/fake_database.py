from backend.persistence.database import Database


class FakeSession():
    pass

class FakeDatabase(Database):

    def __init__(self):
        self.SessionLocal = lambda: FakeSession()

    def create_tables(self):
        SQLAlchemyBase.metadata.create_all(engine)
    