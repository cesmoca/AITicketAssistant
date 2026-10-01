from enum import StrEnum
from ..domain.ticket_action import TicketAction, TicketActionType
from ..domain.task_info import TaskInfo
from .ticket_entity import TicketEntity


class TicketMapper:
    
    @staticmethod
    def to_entity(ticket: TicketAction) -> TicketEntity:
        return TicketEntity(
        ticket_id = ticket.ticket_id,
        name = ticket.info.name,
        appliance = ticket.info.appliance,
        address = ticket.info.address,
        failure = ticket.info.failure,
        other_details = ticket.info.other_details,
        ticket_type = ticket.ticket_type.value,
        )
    
    @staticmethod
    def to_domain(entity: TicketEntity) -> TicketAction:
        return TicketAction(
        ticket_id = entity.ticket_id,
        info = TaskInfo(
            name = entity.name,
            appliance = entity.appliance,
            address = entity.address,
            failure = entity.failure,
            other_details = entity.other_details,
        ),
        ticket_type = TicketActionType(entity.ticket_type)
        )
        
    @staticmethod
    def update_entity(entity: TicketEntity, ticket: TicketAction) -> None:
        entity.name = ticket.info.name
        entity.appliance = ticket.info.appliance
        entity.address = ticket.info.address
        entity.failure = ticket.info.failure
        entity.other_details = ticket.info.other_details
        entity.ticket_type = ticket.ticket_type.value
