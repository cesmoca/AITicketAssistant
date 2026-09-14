from abc import ABC, abstractmethod
from .task import Task

class TaskProcessor(ABC):
    
    @abstractmethod
    def process_task(self, input: str) -> Task:
        pass
        