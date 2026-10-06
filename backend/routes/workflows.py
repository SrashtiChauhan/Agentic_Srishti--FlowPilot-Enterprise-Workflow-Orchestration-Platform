from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from backend.database.database import get_db
from backend.database.models.workflow import WorkflowDB
from sqlalchemy import select


router=APIRouter(
    prefix="/workflows",
    tags=["Workflows"],

)

@router.get("/")
async def get_workflows(db:Session=Depends(get_db)):
    result=db.execute(select(WorkflowDB))
    workflows=result.scalars().all()
    return{
        "message":"Workflows endpoint is working",
        "workflows":workflows
    }