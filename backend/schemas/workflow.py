from pydantic import BaseModel
from typing import Literal
from backend.models.workflow import WorkflowNode , WorkflowEdge
from backend.schemas.workflow import WorkflowCreate
class WorkflowCreate(BaseModel):
    name:str
    description:str|None=None
    status: Literal["Draft", "Active", "Paused"] = "Draft"
    nodes:list[WorkflowNode]=[]
    edges:list[WorkflowEdge]=[]