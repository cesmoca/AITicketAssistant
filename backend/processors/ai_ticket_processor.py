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
            return ProcessTicketResult(status="Ticket added", result=ticket)
        
        elif ticket_action.action_type == "update":
            candidates = self.repository.searchTicket(ticket_action)

            if len(candidates) == 1:
                ticket = candidates[0]
                self._applyActionTicket(ticket_action, ticket)
                self.repository.update(ticket)
                return ProcessTicketResult(status="resolution_required", result=ticket)

            else:
                return ProcessTicketResult(status="resolution_required", result=None)

        elif ticket_action.action_type == "cancel":
            candidates = self.repository.searchTicket(ticket_action)

            if len(candidates) == 1:
                ticket = candidates[0]
                self.repository.delete(ticket.id)
                return ProcessTicketResult(status="resolution_required", result=ticket)

            else:
                return ProcessTicketResult(
                    status="resolution_required", data=None, result=None
                )

        else:
            pprint(
                f"Undetermined database action for ticket type: {ticket_action.action_type}"
            )
            return ProcessTicketResult(status="ok", data=None, result=None)

    def _applyActionTicket(self, ticketAction: TicketAction, ticket: Ticket):

        if ticketAction.info.name is None:
            ticketAction.info.name = ticket.info.name

        if ticketAction.info.appliance is None:
            ticketAction.info.appliance = ticket.info.appliance

        if ticketAction.info.address is None:
            ticketAction.info.address = ticket.info.address

        if ticketAction.info.failure is None:
            ticketAction.info.failure = ticket.info.failure
