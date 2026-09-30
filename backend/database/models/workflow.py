from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class WorkflowDB(Base):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Draft",
    )
    nodes:Mapped[list]=mapped_column(JSON, nullable=False, default=list)
    edges:Mapped[list]=mapped_column(JSON, nullable=False, default=list)