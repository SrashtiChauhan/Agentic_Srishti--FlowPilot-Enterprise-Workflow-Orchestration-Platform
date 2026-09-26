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
WorkflowNodeStatus=Literal [
    "idle",
    "running",
    "completed",
    "failed",
    "waiting_approval",
]

class WorkflowNodePosition(BaseModel):
    x:float
    y:float


class WorkflowNode(BaseModel):
    id:str
    type:str
    title:str
    subtitle:str | None=None
    position:WorkflowNodePosition
    status:WorkflowNodeStatus

class Workflow(BaseModel):
    id:str
    name:str
    description: str | None = None
    status: Literal["Draft", "Active", "Paused"]
