import asyncio

from backend.agent.graph import research_graph


INITIAL_STATE = {
    "question": "How is India positioned in the AI chip industry?",
    "research_iteration": 0,
    "max_iterations": 3,
    "max_sources": 40,
    "search_queries": [],
    "search_results": [],
    "fetched_content": [],
    "failed_fetches": [],
    "claims": [],
}


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_node(node_name: str) -> None:
    print("\n" + "-" * 60)
    print(f"NODE: {node_name}")
    print("-" * 60)


def print_update(state_update: dict) -> None:
    if "research_id" in state_update:
        print("Research ID:", state_update["research_id"])

    if "search_queries" in state_update:
        queries = state_update["search_queries"]

        print(f"\nSEARCH QUERIES: {len(queries)}")

        for index, query in enumerate(queries, start=1):
            print(f"{index}. {query}")

    if "search_results" in state_update:
        results = state_update["search_results"]

        print(f"\nSEARCH RESULTS: {len(results)}")

        for result in results[:5]:
            print(f"- {result.get('title', 'No title')}")
            print(f"  {result.get('url', 'No URL')}")

        if len(results) > 5:
            print(f"... and {len(results) - 5} more")

    if "fetched_content" in state_update:
        fetched = state_update["fetched_content"]

        print(f"\nFETCHED CONTENT: {len(fetched)}")

        for page in fetched[:5]:
            print(f"- {page.get('title', 'No title')}")
            print(f"  {page.get('url', 'No URL')}")

        if len(fetched) > 5:
            print(f"... and {len(fetched) - 5} more")

    if "failed_fetches" in state_update:
        failures = state_update["failed_fetches"]

        print(f"\nFAILED FETCHES: {len(failures)}")

        for failure in failures[:5]:
            print(f"- {failure.get('url', 'Unknown URL')}")
            print(f"  Reason: {failure.get('reason', 'Unknown')}")

    if "research_complete" in state_update:
        print("\nRESEARCH EVALUATION")
        print("Complete:", state_update["research_complete"])
        print(
            "Terminated:",
            state_update.get("research_terminated", False),
        )
        print(
            "Reason:",
            state_update.get("completeness_reason", ""),
        )
        print(
            "Missing aspects:",
            state_update.get("missing_aspects", []),
        )
        print(
            "Termination reason:",
            state_update.get("termination_reason", ""),
        )
        print(
            "Iteration:",
            state_update.get("research_iteration", 0),
        )

    if "claims" in state_update:
        claims = state_update["claims"]

        print(f"\nEXTRACTED CLAIMS: {len(claims)}")

        for index, claim in enumerate(claims[:10], start=1):
            print(f"\nCLAIM {index}")
            print("Statement:", claim.get("statement"))
            print("Type:", claim.get("claim_type"))
            print("Source:", claim.get("source_title"))
            print("URL:", claim.get("source_url"))
            print("Evidence:", claim.get("evidence"))

        if len(claims) > 10:
            print(f"\n... and {len(claims) - 10} more claims")

    if "research_id" in state_update:
        print(
            "\nResearch session:",
            state_update["research_id"],
        )

    if "synthesis" in state_update:
        print("\nSYNTHESIS")
        print(state_update["synthesis"])


async def main() -> None:
    print_header("ARIA GRAPH TEST")

    async for event in research_graph.astream(
        INITIAL_STATE,
        stream_mode="updates",
    ):
        if not event:
            continue

        for node_name, state_update in event.items():
            print_node(node_name)

            if state_update is None:
                print(
                    "WARNING: node returned None instead of a state update."
                )
                continue

            if not isinstance(state_update, dict):
                print(
                    "WARNING: unexpected state update type:",
                    type(state_update).__name__,
                )
                print(state_update)
                continue

            print_update(state_update)

    print_header("ARIA GRAPH TEST FINISHED")


if __name__ == "__main__":
    asyncio.run(main())