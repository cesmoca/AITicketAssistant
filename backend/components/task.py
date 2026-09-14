
from pydantic import BaseModel

class Task(BaseModel):
    name: str | None
    appliance: str | None
    address: str | None
    failure: str | None