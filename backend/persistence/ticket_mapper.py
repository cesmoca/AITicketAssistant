from enum import StrEnum
from ..domain.ticket_action import TicketAction, TicketActionType
from .ticket_entity import TicketEntity


class TicketMapper:
    
    @staticmethod
    def to_entity(ticket: TicketAction) -> TicketEntity:
        return TicketEntity(
        ticket_id = ticket.ticket_id,
        name = ticket.name,
        appliance = ticket.appliance,
        address = ticket.address,
        failure = ticket.failure,
        other_details = ticket.other_details,
        ticket_type = ticket.ticket_type.value,
        )
    
    @staticmethod
    def to_domain(entity: TicketEntity) -> TicketAction:
        return TicketAction(
        ticket_id = entity.ticket_id,
        name = entity.name,
        appliance = entity.appliance,
        address = entity.address,
        failure = entity.failure,
        other_details = entity.other_details,
        ticket_type = TicketActionType(entity.ticket_type)
        )
        
    @staticmethod
    def update_entity(entity: TicketEntity, ticket: TicketAction) -> None:
        entity.name = ticket.name
        entity.appliance = ticket.appliance
        entity.address = ticket.address
        entity.failure = ticket.failure
        entity.other_details = ticket.other_details
        entity.ticket_type = ticket.ticket_type.value