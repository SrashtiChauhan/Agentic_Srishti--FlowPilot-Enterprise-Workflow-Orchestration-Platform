from pydantic import BaseModel, Field
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

class WorkflowNodeConfig(BaseModel):
    agentId:str|None=None
    triggerType:Literal["webhook", "schedule", "event", "manual"] | None=None
    actionType:Literal["slack", "jira", "email", "database", "github","api",] | None=None
    conditionLogic:str|None=None
    prompt:str|None=None
    temperature:float | None=Field(default=None,ge=0,le=1)
    riskScore: Literal["low", "medium","high","critical"] | None=None
    requireApprovalRole: str | None=None



class WorkflowNode(BaseModel):
    id:str
    type:str
    title:str
    subtitle:str | None=None
    position:WorkflowNodePosition
    status:WorkflowNodeStatus
    config:WorkflowNodeConfig

class Workflow(BaseModel):
    id:str
    name:str
    description: str | None = None
    status: Literal["Draft", "Active", "Paused"]
