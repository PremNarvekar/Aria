from typing import Annotated, Any, TypedDict
import operator


class AgentState(TypedDict, total=False):
    # -----------------------------
    # User input
    # -----------------------------
    question: str

    # -----------------------------
    # Research planning
    # -----------------------------
    search_queries: Annotated[
        list[str],
        operator.add,
    ]

    # -----------------------------
    # Search results
    # -----------------------------
    search_results: Annotated[
        list[dict[str, Any]],
        operator.add,
    ]

    # -----------------------------
    # Fetched web content
    # -----------------------------
    fetched_content: Annotated[
        list[dict[str, Any]],
        operator.add,
    ]

    # -----------------------------
    # Fetch failures
    # -----------------------------
    failed_fetches: Annotated[
        list[dict[str, Any]],
        operator.add,
    ]

    # ----------------------------
    # Research evaluation
    # ----------------------------
    research_complete: bool
    completeness_reason: str
    missing_aspects: list[str]

    # -----------------------------
    # Research control
    # -----------------------------
    research_iteration: int
    max_iterations: int

    max_sources: int

    # -----------------------------
    # Termination
    # -----------------------------

    research_terminated: bool
    termination_reason: str
    
    