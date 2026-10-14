
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models.agent import AgentDB
from backend.models.agent import AgentConfig

from fastapi import HTTPException



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


@router.get("/")
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(AgentDB).order_by(AgentDB.name).all()

    return {
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "provider": agent.provider,
                "model_name": agent.model_name,
                "system_prompt": agent.system_prompt,
                "temperature": agent.temperature,
                "tool_bindings": agent.tool_bindings,
                "risk_score": agent.risk_score,
            }
            for agent in agents
        ]
    }

@router.get("/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(AgentDB).filter(AgentDB.id == agent_id).first()

    if agent is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "provider": agent.provider,
        "model_name": agent.model_name,
        "system_prompt": agent.system_prompt,
        "temperature": agent.temperature,
        "tool_bindings": agent.tool_bindings,
        "risk_score": agent.risk_score,
    }


@router.put("/{agent_id}")
def update_agent(
    agent_id: str,
    agent_data: AgentConfig,
    db: Session = Depends(get_db),
):
    agent = (
        db.query(AgentDB)
        .filter(AgentDB.id == agent_id)
        .first()
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    agent.name = agent_data.name
    agent.description = agent_data.description
    agent.provider = agent_data.provider
    agent.model_name = agent_data.model_name
    agent.system_prompt = agent_data.system_prompt
    agent.temperature = agent_data.temperature
    agent.tool_bindings = agent_data.tool_bindings
    agent.risk_score = agent_data.risk_score

    db.commit()
    db.refresh(agent)

    return {
        "message": "Agent updated successfully",
        "agent": {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "provider": agent.provider,
            "model_name": agent.model_name,
            "system_prompt": agent.system_prompt,
            "temperature": agent.temperature,
            "tool_bindings": agent.tool_bindings,
            "risk_score": agent.risk_score,
        },
    }


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    agent = (
        db.query(AgentDB)
        .filter(AgentDB.id == agent_id)
        .first()
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    db.delete(agent)
    db.commit()

    return {
        "message": "Agent deleted successfully",
        "id": agent_id,
    }