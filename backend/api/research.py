import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from ..agent.graph import research_graph
from ..services.research_event import research_events
from ..services.research_store import (
    create_research_session,
    get_research_session,
    update_research_session,
)
from .auth import get_current_user


router = APIRouter(
    prefix="/api/research",
    tags=["research"],
)


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=5,
        max_length=1000,
    )


class ResearchResponse(BaseModel):
    research_id: str
    question: str
    status: str
    report: dict | None = None
    sources: list[dict[str, Any]] = []
    indexed_chunks: int = 0
    rag_indexed: bool = False
    error: str | None = None


# The heavy research execution has been moved to backend.worker.tasks
from ..worker.tasks import execute_research_task


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=202,
)
async def create_research(
    request: ResearchRequest,
    user_id: str = Depends(get_current_user),
) -> ResearchResponse:

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Research question cannot be empty.",
        )

    session = await create_research_session(
        question,
        user_id=user_id,
    )

    research_id = session["research_id"]

    # Send to Celery worker instead of running in the local FastAPI event loop
    execute_research_task.delay(
        session["research_id"],
        request.question,
    )

    return ResearchResponse(
        research_id=research_id,
        question=question,
        status="queued",
    )


@router.get(
    "/{research_id}",
    response_model=ResearchResponse,
)
async def get_research(
    research_id: str,
    user_id: str = Depends(get_current_user),
) -> ResearchResponse:

    session = await get_research_session(
        research_id=research_id,
        user_id=user_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Research session not found.",
        )

    return ResearchResponse(
        research_id=session["research_id"],
        question=session["question"],
        status=session["status"],
        report=session.get("report"),
        sources=session.get(
            "sources",
            [],
        ),
        indexed_chunks=session.get(
            "indexed_chunks",
            0,
        ),
        rag_indexed=session.get(
            "rag_indexed",
            False,
        ),
        error=session.get("error"),
    )