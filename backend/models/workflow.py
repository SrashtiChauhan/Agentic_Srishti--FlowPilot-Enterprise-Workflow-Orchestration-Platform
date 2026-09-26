from pydantic import BaseModel
from typing import Literal
WorkflowNodeType = Literal[
    "trigger",
    "agent",
    "condition",
    "hitl",
    "action",
    "webhook",
]


class WorkflowNode(BaseModel):
    id:str
    type:str
    title:str
    subtitle:str | None=None

class Workflow(BaseModel):
    id:str
    name:str
    description: str | None = None
    status: Literal["Draft", "Active", "Paused"]
