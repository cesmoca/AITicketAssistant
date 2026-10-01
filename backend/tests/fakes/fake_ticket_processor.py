from backend.domain.task_info import TaskInfo
from backend.domain.ticket import Ticket, TicketStatus
from backend.processors.ticket_processor import (
    ProcessTicketRequest,
    ProcessTicketResult,
    TicketProcessor,
)


class FakeTicketProcessor(TicketProcessor):
    def process_ticket(self, request: ProcessTicketRequest) -> ProcessTicketResult:
        ticket = Ticket(
            id=1,
            info=TaskInfo(
                name="Pedro",
                appliance="Antena",
                address="Calle agua",
                failure=f"FAKE: {request.text}",
                other_details="Tiene prisa",
            ),
            status=TicketStatus.ACTIVE,
        )
        return ProcessTicketResult(status="ok", data=None, result=ticket)
