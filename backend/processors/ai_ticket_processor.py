from pydantic import BaseModel
from pprint import pprint
from .ticket_processor import TicketProcessor
from ..domain.ticket_action import TicketAction, TicketActionType

class ProcessTicketRequest(BaseModel):
    text: str
    
class ProcessTicketResult(BaseModel):
    status: str
    result: TicketAction | None

    
class AITicketProcessor(TicketProcessor):
    
    def __init__(self, repository, ticket_ai):
        self.repository = repository 
        self.ticket_ai = ticket_ai
    
    def process_ticket(self, input: str) -> ProcessTicketResult:
        ticket = self.ticket_ai.request_ai(input)
        pprint(ticket)
        
        if ticket.ticket_type == "new":
            self.repository.create(ticket)
            
        elif ticket.ticket_type == "update":
            candidates = self.repository.searchTicket(ticket)
            
            if len(candidates) == 1:
                self._updateTicket(ticket, candidates[0])
                self.repository.update(ticket)
            else:
                return ProcessTicketResult(status="resolution_required", result=None)

                
        elif ticket.ticket_type == "cancel":
            candidates = self.repository.searchTicket(ticket)
            
            candidates = self.repository.searchTicket(ticket)
            
            if len(candidates) == 1:
                self.repository.delete(candidates[0].ticket_id)
            else:
                return ProcessTicketResult(status="resolution_required", result=None)
                
        else:
            pprint(f"Undetermined database action for ticket type: {ticket.ticket_type}")
            
        return ProcessTicketResult(status="ok", result=ticket)
    
    def _updateTicket(self, toTicket: TicketAction, fromTicket: TicketAction):
        
        toTicket.ticket_id = fromTicket.ticket_id
        if toTicket.info.name is None:
            toTicket.info.name = fromTicket.info.name
            
        if toTicket.info.appliance is None:
            toTicket.info.appliance = fromTicket.info.appliance
            
        if toTicket.info.address is None:
            toTicket.info.address = fromTicket.info.address
            
        if toTicket.info.failure is None:
            toTicket.info.failure = fromTicket.info.failure
            
        
        
    
