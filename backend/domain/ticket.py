from enum import Enum

from pydantic import BaseModel

from .task_info import TaskInfo


class TicketStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    OTHER = "other"


class Ticket(BaseModel):
    id: int
    info: TaskInfo
    status: TicketStatus
