from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..rag.followup import followup_service

from ..agent.graph import research_graph
from ..services.research_store import (
    create_research_session,
    get_research_session,
    update_research_session,
)


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
    indexed_chunks: int = 0
    rag_indexed: bool = False
    error: str | None = None
    
class FollowUpRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=1000
    )
    
class FollowUpResponse(BaseModel):
    research_id: str
    question: str
    answer: str
    sources: list[dict[str, str]]

async def run_research(
    research_id: str,
    question: str,
) -> None:

    update_research_session(
        research_id,
        status="running",
    )

    initial_state: dict[str, Any] = {
        "question": question,
        "research_id": research_id,
        "research_iteration": 0,
        "max_iterations": 5,
        "max_sources": 20,
        "search_queries": [],
        "search_results": [],
        "fetched_content": [],
        "failed_fetches": [],
        "claims": [],
    }

    try:
        final_state = await research_graph.ainvoke(
            initial_state,
        )

        update_research_session(
            research_id,
            status="completed",
            report=final_state.get("report"),
            sources=final_state.get(
                "fetched_content",
                [],
            ),
            indexed_chunks=final_state.get(
                "indexed_chunks",
                0,
            ),
            rag_indexed=final_state.get(
                "rag_indexed",
                False,
            ),
        )

    except Exception as exc:

        update_research_session(
            research_id,
            status="failed",
            error=str(exc),
        )


@router.post(
    "",
    response_model=ResearchResponse,
)
async def create_research(
    request: ResearchRequest,
) -> ResearchResponse:

    question = request.question.strip()

    session = create_research_session(
        question,
    )

    research_id = session["research_id"]

    import asyncio

    asyncio.create_task(
        run_research(
            research_id,
            question,
        )
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
) -> ResearchResponse:

    session = get_research_session(
        research_id,
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
    
@router.post(
    "/{research_id}/followup",
    response_model=FollowUpResponse,
)
async def create_followup(
    research_id: str,
    request: FollowUpRequest,
) -> FollowUpResponse:

    session = get_research_session(
        research_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Research session not found.",
        )

    if session["status"] != "completed":
        raise HTTPException(
            status_code=409,
            detail="Research is not completed yet.",
        )

    question = request.question.strip()

    try:
        result = await followup_service.answer(
            research_id=research_id,
            question=question,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Follow-up failed: {exc}",
        ) from exc

    return FollowUpResponse(
        research_id=research_id,
        question=question,
        answer=result["answer"],
        sources=result["sources"],
    )