from ..domain.task_info import TaskInfo
from ..domain.ticket import Ticket, TicketStatus
from ..domain.ticket_action import TicketAction
from .ticket_entity import TicketEntity


class TicketMapper:

    @staticmethod
    def to_entity(ticket: Ticket) -> TicketEntity:
        return TicketEntity(
        id = ticket.id,
        name = ticket.info.name,
        appliance = ticket.info.appliance,
        address = ticket.info.address,
        failure = ticket.info.failure,
        other_details = ticket.info.other_details,
        status = ticket.status.value,
        )

    @staticmethod
    def to_domain(entity: TicketEntity) -> Ticket:
        return Ticket(
        id = entity.id,
        info = TaskInfo(
            name = entity.name,
            appliance = entity.appliance,
            address = entity.address,
            failure = entity.failure,
            other_details = entity.other_details,
        ),
        status = TicketStatus(entity.status)
        )

    @staticmethod
    def to_new_ticket(action: TicketAction) -> Ticket:
        return Ticket(
        id = None,
        info = TaskInfo(
            name = action.info.name,
            appliance = action.info.appliance,
            address = action.info.address,
            failure = action.info.failure,
            other_details = action.info.other_details,
        ),
        status = TicketStatus.ACTIVE
        )

    @staticmethod
    def update_entity(entity: TicketEntity, ticket: Ticket) -> None:
        entity.name = ticket.info.name
        entity.appliance = ticket.info.appliance
        entity.address = ticket.info.address
        entity.failure = ticket.info.failure
        entity.other_details = ticket.info.other_details
        entity.status = ticket.status.value
