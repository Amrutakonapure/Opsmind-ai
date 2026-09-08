from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="ENGINEER",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    incidents_created = relationship(
        "Incident",
        foreign_keys="Incident.created_by",
        back_populates="creator"
    )

    incidents_assigned = relationship(
        "Incident",
        foreign_keys="Incident.assigned_to",
        back_populates="assignee"
    )