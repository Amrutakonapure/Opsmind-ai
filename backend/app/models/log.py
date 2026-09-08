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


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False
    )

    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    incident = relationship(
        "Incident",
        back_populates="logs"
    )

    service = relationship(
        "Service",
        back_populates="logs"
    )