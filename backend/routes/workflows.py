from fastapi import APIRouter

router=APIRouter(
    prefix="/workflows",
    tags=["Workflows"],

)

@router.get("/")
async def get_workflows():
    return{
        "message":"Workflows endpoint is working",
        "workflows":[],
    }