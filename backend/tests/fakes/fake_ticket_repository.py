from backend.domain.ticket import Ticket
from backend.domain.ticket_action import TicketAction
from backend.repositories.ticket_repository import TicketRepository


class FakeTicketRepository(TicketRepository):
    def __init__(self):
        self.tickets: dict[int, Ticket] = {}

    def create(self, ticket: Ticket) -> Ticket:
        if not isinstance(ticket, Ticket):
            raise TypeError("create expects Ticket")
        if ticket.id is not None:
            raise ValueError("Cannot create a Ticket that already has an ID")
        ticket = ticket.model_copy(update={"id": max(self.tickets, default=0) + 1})
        self.tickets[ticket.id] = ticket
        return ticket

    def get(self, ticket_id: int) -> Ticket | None:
        return self.tickets.get(ticket_id)

    def update(self, ticket: Ticket) -> Ticket:
        if not isinstance(ticket, Ticket):
            raise TypeError("update expects Ticket")
        self.tickets[ticket.id] = ticket
        return ticket

    def list(self) -> list[Ticket]:
        return list(self.tickets.values())

    def searchTicket(self, ticket: Ticket | TicketAction) -> list[Ticket]:
        return [
            candidate for candidate in self.list()
            if (ticket.info.name is not None and candidate.info.name is not None
                and ticket.info.name.strip().lower() == candidate.info.name.strip().lower())
            or (ticket.info.address is not None and candidate.info.address is not None
                and ticket.info.address.strip().lower() == candidate.info.address.strip().lower())
        ]

    def delete(self, ticket: Ticket) -> bool:
        if ticket is None:
            raise ValueError("Delete should have a valid ticket")
        if ticket.id is None:
            raise ValueError("Delete should have a valid ticket_id")
        return self.tickets.pop(ticket.id, None) is not None

    def clear(self):
        self.tickets.clear()
