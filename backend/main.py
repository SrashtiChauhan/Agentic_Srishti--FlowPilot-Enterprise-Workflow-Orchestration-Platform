from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.workflows import router as workflow_router

app=FastAPI(
    title="FlowPilot API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(workflow_router)

@app.get("/health")
async def health_check():
    return{
        "status":"ok",
        "service":"flowpilot-ai",
    }