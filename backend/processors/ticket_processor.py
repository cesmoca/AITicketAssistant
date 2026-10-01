from abc import ABC, abstractmethod
from ..domain.ticket_action import TicketAction

class TicketProcessor(ABC):
    
    @abstractmethod
    def process_ticket(self, input: str) -> TicketAction:
        pass
        