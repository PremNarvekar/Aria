import asyncio

from backend.agent.nodes import (
    initialize_research,
    plan_research,
    execute_research,
    fetch_content,
    check_completeness,
    extract_claims,
    synthesise,
    index_research,
)


async def main():

    state = {
        "question": (
            "How is India positioned "
            "in the AI chip industry?"
        ),
        "research_iteration": 0,
        "max_iterations": 3,
        "max_sources": 40,
        "search_queries": [],
        "search_results": [],
        "fetched_content": [],
        "failed_fetches": [],
        "claims": [],
    }

    print("=" * 60)
    print("ARIA NODE TEST")
    print("=" * 60)

    # Initialize
    print("\n[1] initialize_research")

    update = initialize_research(state)
    state.update(update)

    print(
        "research_id:",
        state.get("research_id"),
    )

    # Planning
    print("\n[2] plan_research")

    update = plan_research(state)
    state.update(update)

    print(
        "queries:",
        len(state.get("search_queries", [])),
    )

    for query in state["search_queries"]:
        print("-", query)

    # Search
    print("\n[3] execute_research")

    update = execute_research(state)
    state.update(update)

    print(
        "search results:",
        len(state.get("search_results", [])),
    )

    # Fetch
    print("\n[4] fetch_content")

    update = await fetch_content(state)
    state.update(update)

    print(
        "fetched pages:",
        len(state.get("fetched_content", [])),
    )

    # Completeness
    print("\n[5] check_completeness")

    update = check_completeness(state)
    state.update(update)

    print(
        "complete:",
        state.get("research_complete"),
    )

    print(
        "terminated:",
        state.get("research_terminated"),
    )

    # Claims
    print("\n[6] extract_claims")

    update = await extract_claims(state)
    state.update(update)

    print(
        "claims:",
        len(state.get("claims", [])),
    )

    # Synthesis
    print("\n[7] synthesise")

    update = synthesise(state)
    state.update(update)

    print(
        "report generated:",
        bool(state.get("report")),
    )

    # RAG indexing
    print("\n[8] index_research")

    update = index_research(state)
    state.update(update)

    print(
        "indexed chunks:",
        state.get("indexed_chunks"),
    )

    print(
        "RAG indexed:",
        state.get("rag_indexed"),
    )

    print("\n" + "=" * 60)
    print("NODE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())