import asyncio

from backend.agent.graph import research_graph
from backend.rag.followup import answer_followup


async def main():

    initial_state = {
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

    final_state = {}

    print("\n" + "=" * 60)
    print("ARIA END-TO-END TEST")
    print("=" * 60)

    async for event in research_graph.astream(
        initial_state,
        stream_mode="updates",
    ):

        for node_name, update in event.items():

            print(
                f"\nCompleted node: {node_name}"
            )

            final_state.update(update)

    research_id = final_state.get(
        "research_id"
    )

    if not research_id:

        raise RuntimeError(
            "Research ID was not returned by the graph."
        )

    print(
        "\nResearch ID:",
        research_id,
    )

    if not final_state.get(
        "rag_indexed",
        False,
    ):

        raise RuntimeError(
            "Research was not indexed into RAG."
        )

    print(
        "RAG indexing: SUCCESS"
    )

    print(
        "Indexed chunks:",
        final_state.get(
            "indexed_chunks",
            0,
        ),
    )

    question = (
        "What are India's biggest challenges "
        "in developing AI chips?"
    )

    print(
        "\nFOLLOW-UP QUESTION:"
    )

    print(question)

    result = answer_followup(
        question=question,
        research_id=research_id,
    )

    print(
        "\nFOLLOW-UP ANSWER:"
    )

    print(
        result["answer"]
    )

    print(
        "\nCONFIDENCE:"
    )

    print(
        result["confidence"]
    )

    print(
        "\nSOURCES:"
    )

    for source in result["sources"]:

        print(
            f"- {source['title']}"
        )

        print(
            f"  {source['url']}"
        )

    print("\n" + "=" * 60)
    print("END-TO-END TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())