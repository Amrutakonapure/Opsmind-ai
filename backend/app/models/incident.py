from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="OPEN",
        nullable=False
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    service = relationship(
        "Service",
        back_populates="incidents"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="incidents_created"
    )

    assignee = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="incidents_assigned"
    )

    comments = relationship(
        "IncidentComment",
        back_populates="incident",
        cascade="all, delete-orphan"
    )

    logs = relationship(
        "Log",
        back_populates="incident",
        cascade="all, delete-orphan"
    )

    ai_analyses = relationship(
        "AIAnalysis",
        back_populates="incident",
        cascade="all, delete-orphan"
    )