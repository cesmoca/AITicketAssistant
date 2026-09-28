from abc import ABC, abstractmethod

class Database(ABC):

    #SessionLocal

    @abstractmethod
    def create_tables():
        pass
    