from pydantic import BaseModel
from enum import Enum
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