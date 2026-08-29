import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ResearchStatus(str, enum.Enum):
    """
    Valid lifecycle states for a research session.

    queued    → created, waiting to start
    running   → agent pipeline is executing
    completed → research finished successfully
    failed    → research terminated with an error
    """

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchSession(Base):

    __tablename__ = "research_sessions"

    research_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    user_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
        default=ResearchStatus.QUEUED.value,
    )

    report: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
    )

    sources: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    indexed_chunks: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    rag_indexed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utc_now,
        onupdate=_utc_now,
    )

    def __repr__(self) -> str:
        return (
            f"<ResearchSession "
            f"id={self.research_id!r} "
            f"status={self.status!r} "
            f"question={self.question[:50]!r}>"
        )