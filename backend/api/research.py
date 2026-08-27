from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..agent.graph import research_graph


router = APIRouter(
    prefix="/api/research",
    tags=["research"],
)


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=5,
        max_length=1000,
        description="Research question to investigate.",
    )


class ResearchResponse(BaseModel):
    research_id: str
    question: str
    status: str
    report: dict | None = None
    indexed_chunks: int = 0
    rag_indexed: bool = False


@router.post(
    "",
    response_model=ResearchResponse,
)
async def create_research(
    request: ResearchRequest,
) -> ResearchResponse:

    initial_state = {
        "question": request.question.strip(),
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
            initial_state
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Research execution failed: {exc}",
        ) from exc

    research_id = final_state.get("research_id")

    if not research_id:
        raise HTTPException(
            status_code=500,
            detail="Research completed without a research_id.",
        )

    return ResearchResponse(
        research_id=research_id,
        question=final_state["question"],
        status="completed",
        report=final_state.get("report"),
        indexed_chunks=final_state.get(
            "indexed_chunks",
            0,
        ),
        rag_indexed=final_state.get(
            "rag_indexed",
            False,
        ),
    )