
from sqlalchemy import Float, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class AgentDB(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
    )

    provider: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="ollama",
    )

    model_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="",
    )

    system_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.2,
    )

    tool_bindings: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    risk_score: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="low",
    )
