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
            self.repository.create(TicketMapper.to_new_ticket(ticket_action))

        elif ticket_action.action_type == "update":
            candidates = self.repository.searchTicket(ticket_action)


            if len(candidates) == 1:

                self._updateTicket(ticket_action, candidates[0])

                self.repository.update(ticket_action)

            else:

                return ProcessTicketResult(status="resolution_required", result=None)


        elif ticket_action.action_type == "cancel":

            candidates = self.repository.searchTicket(ticket_action)

            if len(candidates) == 1:

                self.repository.delete(candidates[0].id)

            else:
                return ProcessTicketResult(status="resolution_required", data=None, result=None)


        else:
            pprint(f"Undetermined database action for ticket type: {ticket_action.action_type}")


        return ProcessTicketResult(status="ok", result=ticket_action)


    def _updateTicket(self, toTicket: TicketAction, fromTicket: Ticket):



        if toTicket.info.name is None:

            toTicket.info.name = fromTicket.info.name


        if toTicket.info.appliance is None:

            toTicket.info.appliance = fromTicket.info.appliance


        if toTicket.info.address is None:

            toTicket.info.address = fromTicket.info.address


        if toTicket.info.failure is None:

            toTicket.info.failure = fromTicket.info.failure
