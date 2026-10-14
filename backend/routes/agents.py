
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models.agent import AgentDB
from backend.models.agent import AgentConfig


router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post("/")
def create_agent(
    agent: AgentConfig,
    db: Session = Depends(get_db),
):
    new_agent = AgentDB(
        id=str(uuid.uuid4()),
        name=agent.name,
        description=agent.description,
        provider=agent.provider,
        model_name=agent.model_name,
        system_prompt=agent.system_prompt,
        temperature=agent.temperature,
        tool_bindings=agent.tool_bindings,
        risk_score=agent.risk_score,
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return {
        "message": "Agent created successfully",
        "agent": {
            "id": new_agent.id,
            "name": new_agent.name,
            "description": new_agent.description,
            "provider": new_agent.provider,
            "model_name": new_agent.model_name,
            "system_prompt": new_agent.system_prompt,
            "temperature": new_agent.temperature,
            "tool_bindings": new_agent.tool_bindings,
            "risk_score": new_agent.risk_score,
        },
    }
