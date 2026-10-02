from sqlalchemy.sql import delete, select

from ..domain.ticket import Ticket
from ..domain.ticket_action import TicketAction
from ..persistence.ticket_entity import TicketEntity
from ..persistence.ticket_mapper import TicketMapper
from .ticket_repository import TicketRepository


class SQLAlchemyTicketRepository(TicketRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, ticket: Ticket) -> Ticket:

        if ticket.id is not None:
            raise ValueError("Cannot create a Ticket that already has an ID")

        with self.session_factory() as session:
            entity = TicketMapper.to_entity(ticket)

            session.add(entity)
            session.commit()

            session.refresh(entity)

            return TicketMapper.to_domain(entity)

    def get(self, ticket_id: int) -> Ticket | None:
        statement = select(TicketEntity).where(TicketEntity.id == ticket_id)

        with self.session_factory() as session:
            entity = session.scalar(statement)

            if entity is None:
                return None

            return TicketMapper.to_domain(entity)

    def update(self, ticket: Ticket) -> Ticket:
        if ticket.id is None:
            raise ValueError("The ticket should have an id")

        statement = select(TicketEntity).where(TicketEntity.id == ticket.id)

        with self.session_factory() as session:
            old_entity = session.scalar(statement)
            if old_entity is None:
                raise ValueError(f"Could not find a Ticket with id {ticket.id}")

            TicketMapper.update_entity(old_entity, ticket)
            session.commit()
            session.refresh(old_entity)

            return TicketMapper.to_domain(old_entity)

    def list(self) -> list[Ticket]:
        statement = select(TicketEntity)

        with self.session_factory() as session:
            entities_list = session.scalars(statement=statement).all()
            return [TicketMapper.to_domain(entity) for entity in entities_list]

    def searchTicket(self, ticket: Ticket | TicketAction) -> list[Ticket]:
        all_tickets: list[Ticket] = self.list()
        candidate_tickets = [
            candidate_ticket
            for candidate_ticket in all_tickets
            if self._areTicketsSimilar(ticket, candidate_ticket)
        ]
        return candidate_tickets

    def delete(self, ticket_id: int) -> bool:

        if ticket_id is None:
            raise ValueError("Delete should have a valid ticket_id")

        with self.session_factory() as session:
            ticket = session.get(TicketEntity, ticket_id)

            if ticket is None:
                return False

            session.delete(ticket)
            session.commit()

            return True

    def clear(self):
        with self.session_factory() as session:
            session.execute(delete(TicketEntity))
            session.commit()

    def _areTicketsSimilar(
        self, ticket1: Ticket | TicketAction, ticket2: Ticket
    ) -> bool:
        if (
            ticket1.info.name is not None
            and ticket2.info.name is not None
            and ticket1.info.name.strip().lower() == ticket2.info.name.strip().lower()
        ):
            return True

        return (
            ticket1.info.address is not None
            and ticket2.info.address is not None
            and ticket1.info.address.strip().lower()
            == ticket2.info.address.strip().lower()
        )
