from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from backend.database.database import get_db

router=APIRouter(
    prefix="/workflows",
    tags=["Workflows"],

)

@router.get("/")
async def get_workflows(db:Session=Depends(get_db)):
    return{
        "message":"Workflows endpoint is working",
        "workflows":[],
    }