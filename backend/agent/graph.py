from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from .state import AgentState

from .nodes import (
    plan_research,
    execute_research,
    fetch_content,
    check_completeness,
)


# ============================================================
# Routing
# ============================================================

def route_after_completeness(
    state: AgentState,
) -> str:

    if state.get(
        "research_terminated",
        False,
    ):
        return "complete"

    return "research_again"


# ============================================================
# Graph Builder
# ============================================================

def build_research_graph():

    workflow = StateGraph(
        AgentState
    )

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    workflow.add_node(
        "plan_research",
        plan_research,
    )

    workflow.add_node(
        "execute_research",
        execute_research,
    )

    workflow.add_node(
        "fetch_content",
        fetch_content,
    )

    workflow.add_node(
        "check_completeness",
        check_completeness,
    )

    # --------------------------------------------------------
    # Initial flow
    # --------------------------------------------------------

    workflow.add_edge(
        START,
        "plan_research",
    )

    workflow.add_edge(
        "plan_research",
        "execute_research",
    )

    workflow.add_edge(
        "execute_research",
        "fetch_content",
    )

    workflow.add_edge(
        "fetch_content",
        "check_completeness",
    )

    # --------------------------------------------------------
    # Research loop
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "check_completeness",
        route_after_completeness,
        {
            "research_again": "plan_research",
            "complete": END,
        },
    )

    return workflow.compile()


research_graph = build_research_graph()