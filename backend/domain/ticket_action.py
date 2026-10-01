from enum import Enum

from pydantic import BaseModel

from .task_info import TaskInfo


class TicketActionType(str, Enum):


    NEW = "new"


    UPDATE = "update"


    CANCEL = "cancel"


    UNDETERMINED = "undetermined"



class TicketAction(BaseModel):
    info: TaskInfo
    action_type: TicketActionType