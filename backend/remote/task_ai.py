from abc import ABC, abstractmethod
from ..domain.task import Task

class TaskAI(ABC):
    
    @abstractmethod
    def request_ai(self, input: str) -> Task:
        pass
        