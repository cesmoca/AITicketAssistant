from backend.domain.ticket_action import TicketAction
from backend.processors.ticket_processor import ProcessTicketRequest
from backend.remote.ticket_ai import TicketAI


class FakeTicketAI(TicketAI):
    def request_ai(self, request: ProcessTicketRequest) -> TicketAction:
        if not isinstance(request, ProcessTicketRequest):
            raise TypeError("request_ai expects ProcessTicketRequest")
        self.last_request = request
        return self.test_ticket
