"""
PostgreSQL-backed research session store.

Every public function manages its own database session.
Callers do not need to know about SQLAlchemy or sessions.

Returns plain dicts so the rest of the application
(API routes, background tasks, LangGraph nodes)
stays decoupled from the ORM.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import select

from ..db.database import SessionLocal
from ..db.models import ResearchSession, ResearchStatus


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(row: ResearchSession) -> dict[str, Any]:
    """
    Convert a SQLAlchemy ORM object to a plain dict.

    This is the boundary between the ORM layer and the
    rest of the application. Everything above this function
    works with dicts — nothing leaks SQLAlchemy types upward.
    """
    return {
        "research_id": row.research_id,
        "question": row.question,
        "status": row.status,
        "report": row.report,
        "sources": row.sources,
        "indexed_chunks": row.indexed_chunks,
        "rag_indexed": row.rag_indexed,
        "error": row.error,
        "created_at": row.created_at.isoformat(),
        "updated_at": row.updated_at.isoformat(),
    }


async def create_research_session(
    question: str,
    user_id: str,
) -> dict[str, Any]:
    """
    Create a new research session in PostgreSQL.

    Generates a UUID, sets status to 'queued', and returns
    a dict representation of the persisted row.
    """
    research_id = str(uuid4())

    row = ResearchSession(
        research_id=research_id,
        user_id=user_id,
        question=question,
        status=ResearchStatus.QUEUED.value,
    )

    async with SessionLocal() as session:
        async with session.begin():
            session.add(row)

    return _row_to_dict(row)


async def get_research_session(
    research_id: str,
    user_id: str = None,
) -> dict[str, Any] | None:
    """
    Get a research session by ID.
    If user_id is provided, enforces that the session belongs to that user.
    """
    async with SessionLocal() as session:
        row = await session.get(
            ResearchSession,
            research_id,
        )

        if row is None:
            return None
            
        if user_id is not None and row.user_id != user_id:
            return None # Enforce row-level isolation

    return _row_to_dict(row)


async def update_research_session(
    research_id: str,
    **updates: Any,
) -> dict[str, Any] | None:
    """
    Update specific fields on a research session.

    Only the provided keyword arguments are modified.
    `updated_at` is handled automatically by the ORM
    via the `onupdate` column hook.

    Returns None if the session does not exist.
    """
    async with SessionLocal() as session:
        async with session.begin():
            row = await session.get(
                ResearchSession,
                research_id,
            )

            if row is None:
                return None

            for key, value in updates.items():
                if hasattr(row, key):
                    setattr(row, key, value)
        
        await session.refresh(row)

    return _row_to_dict(row)