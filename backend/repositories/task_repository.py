from abc import ABC, abstractmethod
from ..domain.task_action import TaskAction

class TaskRepository(ABC):
    
    @abstractmethod
    def create(self, task: TaskAction) -> TaskAction:
        pass
    
    @abstractmethod
    def update(self, task: TaskAction):
        pass

    @abstractmethod    
    def get(self, id: int) -> TaskAction | None:
        pass

    @abstractmethod
    def list(self) -> list(TaskAction):
        pass
    
    @abstractmethod
    def searchTask(self) -> list(TaskAction):
        pass
    
    @abstractmethod
    def delete(self, task_id) -> Boolean:
        pass
    
    @abstractmethod
    def clear(self):
        pass