
from typing import Literal

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for a FlowPilot AI agent."""

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)

    provider: Literal[
        "ollama",
        "huggingface",
        "mistral",
    ] = "ollama"

    model_name: str = Field(
        default="",
        max_length=200,
    )

    system_prompt: str = Field(
        min_length=1,
        max_length=10000,
    )

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
    )

    tool_bindings: list[str] = Field(
        default_factory=list,
    )

    risk_score: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] = "low"
