from abc import ABC, abstractmethod
from ..domain.ticket_action import TicketAction

class TicketAI(ABC):
    
    @abstractmethod
    def request_ai(self, input: str) -> TicketAction:
        pass
        