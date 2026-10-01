from abc import ABC, abstractmethod
from ..domain.task_action import TaskAction

class TaskProcessor(ABC):
    
    @abstractmethod
    def process_task(self, input: str) -> TaskAction:
        pass
        