
from typing import Literal

from pydantic import BaseModel, Field

from backend.models.workflow import WorkflowNode, WorkflowEdge


class WorkflowCreate(BaseModel):
    name: str
    description: str | None = None
    status: Literal["Draft", "Active", "Paused"] = "Draft"
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)


class WorkflowRunRequest(BaseModel):
    initial_input: str = Field(
        min_length=1,
        max_length=10000,
    )
