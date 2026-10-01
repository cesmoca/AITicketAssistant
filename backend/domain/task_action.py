from pydantic import BaseModel
from enum import Enum

class TaskActionType(str, Enum):
    NEW = "new"
    UPDATE = "update"
    CANCEL = "cancel"
    UNDETERMINED = "undetermined"

class TaskAction(BaseModel):
    task_id: int | None
    name: str | None
    appliance: str | None
    address: str | None
    failure: str | None
    other_details: str|None
    task_type: TaskActionType