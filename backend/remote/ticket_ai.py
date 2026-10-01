from abc import ABC, abstractmethod

from ..domain.ticket_action import TicketAction
from ..processors.ticket_processor import ProcessTicketRequest


class TicketAI(ABC):
    
    @abstractmethod
    def request_ai(self, request: ProcessTicketRequest) -> TicketAction:
        pass
        