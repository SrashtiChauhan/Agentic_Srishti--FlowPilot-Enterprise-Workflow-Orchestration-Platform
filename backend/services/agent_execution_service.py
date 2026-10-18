
from sqlalchemy.orm import Session

from backend.database.models.agent import AgentDB
from backend.services.ollama_service import generate_response


class AgentExecutionError(RuntimeError):
    """Raised when an agent cannot be executed."""


def execute_agent(
    agent_id: str,
    user_input: str,
    db: Session,
) -> dict[str, str]:
    """Load a saved agent and execute it using its configured provider."""

    agent = (
        db.query(AgentDB)
        .filter(AgentDB.id == agent_id)
        .first()
    )

    if agent is None:
        raise AgentExecutionError("Agent not found.")

    if agent.provider != "ollama":
        raise AgentExecutionError(
            f"Provider '{agent.provider}' is not implemented yet."
        )

    if not agent.model_name or not agent.model_name.strip():
        raise AgentExecutionError(
            "The agent does not have a model configured."
        )

    try:
        output = generate_response(
            model_name=agent.model_name,
            system_prompt=agent.system_prompt,
            user_input=user_input,
            temperature=agent.temperature,
        )
    except RuntimeError as exc:
        raise AgentExecutionError(str(exc)) from exc

    return {
        "agent_id": agent.id,
        "agent_name": agent.name,
        "model_name": agent.model_name,
        "output": output,
    }
