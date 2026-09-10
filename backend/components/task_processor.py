from abc import ABC, abstractmethod

class TaskProcessor(ABC):
    
    @abstractmethod
    def process_task(self, input: str) -> str:
        pass
        