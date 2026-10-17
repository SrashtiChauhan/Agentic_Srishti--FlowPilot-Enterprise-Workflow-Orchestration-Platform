
from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    """Input supplied when running a saved agent."""

    user_input: str = Field(
        min_length=1,
        max_length=10000,
    )
