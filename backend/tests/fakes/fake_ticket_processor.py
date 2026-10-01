from backend.processors.ticket_processor import TicketProcessor
from backend.domain.ticket_action import TicketAction, TicketActionType
from backend.processors.ai_ticket_processor import ProcessTicketResult
class FakeTicketProcessor(TicketProcessor):
    
    def process_ticket(self, input: str) -> ProcessTicketResult:
        ticket = TicketAction(
            ticket_id=1,
            name="Pedro",
            appliance="Antena",
            address="Calle agua",
            failure=f"FAKE: {input}",
            other_details="Tiene prisa",            
            ticket_type=TicketActionType.NEW
        )
        
        return ProcessTicketResult(status="ok", result=ticket)