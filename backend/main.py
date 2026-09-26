from fastapi import FastAPI
app=FastAPI(
    title="FlowPilot API",
    version="0.1.0",
)
@app.get("health")
async def health_check():
    return{
        "status":"ok",
        "service":"flowpilot-ai",
    }