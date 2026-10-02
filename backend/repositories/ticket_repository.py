from abc import ABC, abstractmethod

from ..domain.ticket import Ticket
from ..domain.ticket_action import TicketAction


class TicketRepository(ABC):
    
    @abstractmethod
    def create(self, ticket: Ticket) -> Ticket:
        pass
    
    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket:
        pass

    @abstractmethod
    def get(self, id: int) -> Ticket | None:
        pass

    @abstractmethod
    def list(self) -> list[Ticket]:
        pass
    
    @abstractmethod
    def searchTicket(self, ticket: Ticket | TicketAction) -> list[Ticket]:
        pass
    
    @abstractmethod
    def delete(self, ticket: Ticket) -> bool:
        pass
    
    @abstractmethod
    def clear(self):
        pass