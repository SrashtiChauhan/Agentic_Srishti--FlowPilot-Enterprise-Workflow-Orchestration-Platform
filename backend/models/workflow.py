from pydantic import BaseModel
from typing import Literal
class Workflow(BaseModel):
    id:str
    name:str
    description: str | None = None
    status: Literal["Draft", "Active", "Paused"]
