from pprint import pprint

from ..domain.ticket import Ticket
from ..domain.ticket_action import TicketAction
from ..persistence.ticket_mapper import TicketMapper
from .ticket_processor import ProcessTicketRequest, ProcessTicketResult, TicketProcessor


class AITicketProcessor(TicketProcessor):
    def __init__(self, repository, ticket_ai):

        self.repository = repository
        self.ticket_ai = ticket_ai

    def process_ticket(self, request: ProcessTicketRequest) -> ProcessTicketResult:

        ticket_action = self.ticket_ai.request_ai(request)

        pprint(ticket_action)

        if ticket_action.action_type == "new":
            ticket = self.repository.create(TicketMapper.to_new_ticket(ticket_action))
            return ProcessTicketResult(status="ok", data="Ticket added", result=ticket)

        elif ticket_action.action_type == "update":
            candidates = self.repository.searchTicket(ticket_action)

            if len(candidates) == 1:
                ticket = candidates[0]
                self._applyActionTicket(ticket_action, ticket)
                self.repository.update(ticket)
                return ProcessTicketResult(
                    status="error", data="resolution_required", result=ticket
                )

            else:
                return ProcessTicketResult(
                    status="error", data="resolution_required", result=None
                )

        elif ticket_action.action_type == "cancel":
            candidates = self.repository.searchTicket(ticket_action)

            if len(candidates) == 1:
                ticket = candidates[0]
                self.repository.delete(ticket.id)
                return ProcessTicketResult(
                    status="error", data="resolution_required", result=ticket
                )

            else:
                return ProcessTicketResult(
                    status="error", data="resolution_required", result=None
                )

        else:
            pprint(
                f"Undetermined database action for ticket type: {ticket_action.action_type}"
            )
            return ProcessTicketResult(status="ok", data=None, result=None)

    def _applyActionTicket(self, ticketAction: TicketAction, ticket: Ticket):

        if ticketAction.info.name is not None:
            ticket.info.name = ticketAction.info.name

        if ticketAction.info.appliance is not None:
            ticket.info.appliance = ticketAction.info.appliance

        if ticketAction.info.address is not None:
            ticket.info.address = ticketAction.info.address

        if ticketAction.info.failure is not None:
            ticket.info.failure = ticketAction.info.failure

        if ticketAction.info.other_details is not None:
            ticket.info.other_details = ticketAction.info.other_details
