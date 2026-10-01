from backend.remote.ticket_ai import TicketAI

class FakeTicketAI(TicketAI): 

    
    def request_ai(self, text: str) -> TicketAction:
        return self.test_ticket