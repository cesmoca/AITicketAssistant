from pydantic import BaseModel
from enum import Enum

class TicketActionType(str, Enum):
    NEW = "new"
    UPDATE = "update"
    CANCEL = "cancel"
    UNDETERMINED = "undetermined"

class TicketAction(BaseModel):
    ticket_id: int | None
    name: str | None
    appliance: str | None
    address: str | None
    failure: str | None
    other_details: str|None
    ticket_type: TicketActionType