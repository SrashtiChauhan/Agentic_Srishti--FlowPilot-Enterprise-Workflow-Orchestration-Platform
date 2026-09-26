from fastapi import FastAPI
from backend.routes.workflows import router as workflow_router

app=FastAPI(
    title="FlowPilot API",
    version="0.1.0",
)
app.include_router(workflow_router)

@app.get("/health")
async def health_check():
    return{
        "status":"ok",
        "service":"flowpilot-ai",
    }