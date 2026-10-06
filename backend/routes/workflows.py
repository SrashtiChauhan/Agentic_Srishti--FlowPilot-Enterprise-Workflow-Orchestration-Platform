from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models.workflow import WorkflowDB
from backend.schemas.workflow import WorkflowCreate

import uuid


router=APIRouter(
    prefix="/workflows",
    tags=["Workflows"],

)

@router.get("/")
async def get_workflows(db:Session=Depends(get_db)):
    result=db.execute(select(WorkflowDB))
    workflows=result.scalars().all()
    return{
        "message": "Workflows fetched successfully",
        "workflows":workflows,
    }

@router.post("/")
async def create_workflow(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
):
    new_workflow = WorkflowDB(
        id=str(uuid.uuid4()),
        name=workflow.name,
        description=workflow.description,
        status=workflow.status,
        nodes=[node.model_dump() for node in workflow.nodes],
        edges=[edge.model_dump() for edge in workflow.edges],
    )

    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)

    return new_workflow