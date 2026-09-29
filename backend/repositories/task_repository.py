from abc import ABC, abstractmethod
from ..domain.task import Task

class TaskRepository(ABC):
    
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def update(self, task: Task):
        pass

    @abstractmethod    
    def get(self, id: int) -> Task | None:
        pass

    @abstractmethod
    def list(self) -> list(Task):
        pass
    
    @abstractmethod
    def delete(self, task_id) -> Boolean:
        pass
    
    @abstractmethod
    def clear(self):
        pass