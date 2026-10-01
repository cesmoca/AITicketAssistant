from pydantic import BaseModel


class TaskInfo(BaseModel):
    name: str | None
    appliance: str | None
    address: str | None
    failure: str | None
    other_details: str | None
