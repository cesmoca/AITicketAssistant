from abc import ABC, abstractmethod

from pydantic import BaseModel

from ..domain.ticket import Ticket


class ProcessTicketRequest(BaseModel):
    text: str

class ProcessTicketResult(BaseModel):
    status: str
    data: str | None = None
    result: Ticket | None

class TicketProcessor(ABC):

    @abstractmethod
    def process_ticket(self, request: ProcessTicketRequest) -> ProcessTicketResult:
        pass

