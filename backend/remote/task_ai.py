from abc import ABC, abstractmethod
from ..domain.task_action import TaskAction

class TaskAI(ABC):
    
    @abstractmethod
    def request_ai(self, input: str) -> TaskAction:
        pass
        