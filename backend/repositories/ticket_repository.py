from abc import ABC, abstractmethod
from ..domain.ticket_action import TicketAction

class TicketRepository(ABC):
    
    @abstractmethod
    def create(self, ticket: TicketAction) -> TicketAction:
        pass
    
    @abstractmethod
    def update(self, ticket: TicketAction):
        pass

    @abstractmethod    
    def get(self, id: int) -> TicketAction | None:
        pass

    @abstractmethod
    def list(self) -> list(TicketAction):
        pass
    
    @abstractmethod
    def searchTicket(self) -> list(TicketAction):
        pass
    
    @abstractmethod
    def delete(self, ticket_id) -> Boolean:
        pass
    
    @abstractmethod
    def clear(self):
        pass