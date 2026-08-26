from langgraph.graph import END, START, StateGraph

from .state import AgentState
from .nodes import (
    check_completeness,
    execute_research,
    extract_claims,
    fetch_content,
    index_research,
    initialize_research,
    plan_research,
    synthesise,
)


# Decide whether to continue research or finish.
def route_after_completeness(state: AgentState) -> str:
    if state.get("research_terminated", False):
        return "complete"

    return "research_again"


# Build the research workflow.
def build_research_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("initialize_research", initialize_research)
    workflow.add_node("plan_research", plan_research)
    workflow.add_node("execute_research", execute_research)
    workflow.add_node("fetch_content", fetch_content)
    workflow.add_node("check_completeness", check_completeness)
    workflow.add_node("extract_claims", extract_claims)
    workflow.add_node("index_research", index_research)
    workflow.add_node("synthesise", synthesise)

    workflow.add_edge(START, "initialize_research")
    workflow.add_edge("initialize_research", "plan_research")

    workflow.add_edge("plan_research", "execute_research")
    workflow.add_edge("execute_research", "fetch_content")
    workflow.add_edge("fetch_content", "check_completeness")

    workflow.add_conditional_edges(
        "check_completeness",
        route_after_completeness,
        {
            "research_again": "plan_research",
            "complete": "extract_claims",
        },
    )

    workflow.add_edge("extract_claims", "index_research")
    workflow.add_edge("index_research", "synthesise")
    workflow.add_edge("synthesise", END)

    return workflow.compile()


research_graph = build_research_graph()