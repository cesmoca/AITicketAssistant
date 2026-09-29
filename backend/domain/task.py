from pydantic import BaseModel
from enum import Enum

class TaskType(str, Enum):
    NEW = "new"
    UPDATE = "update"
    CANCEL = "cancel"
    UNDETERMINED = "undetermined"

class Task(BaseModel):
    task_id: int | None
    name: str | None
    appliance: str | None
    address: str | None
    failure: str | None
    other_details: str|None
    task_type: TaskType