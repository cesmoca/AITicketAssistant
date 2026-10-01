from enum import Enum

from pydantic import BaseModel

from .task_info import TaskInfo


class TicketActionType(str, Enum):
    NEW = "new"
    UPDATE = "update"
    CANCEL = "cancel"
    UNDETERMINED = "undetermined"

class TicketAction(BaseModel):
    ticket_id: int | None
    info: TaskInfo
    ticket_type: TicketActionType