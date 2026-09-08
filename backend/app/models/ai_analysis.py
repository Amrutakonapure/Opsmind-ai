from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Float,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    probable_cause: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    incident = relationship(
        "Incident",
        back_populates="ai_analyses"
    )