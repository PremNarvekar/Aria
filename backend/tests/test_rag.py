from backend.rag.store import index_research
from backend.rag.session import create_research_id
from backend.rag.followup import answer_followup


def main():
    research_id = create_research_id()

    research = [
        {
            "title": "India Semiconductor Research",
            "url": "https://example.com/india-semiconductor",
            "query": "India semiconductor industry",
            "content": """
            India is developing semiconductor manufacturing
            capabilities through government incentives,
            semiconductor fabrication projects, and investments
            in chip design and manufacturing infrastructure.
            """,
        },
        {
            "title": "India AI Chip Research",
            "url": "https://example.com/india-ai-chips",
            "query": "India AI chip industry",
            "content": """
            Indian companies and research organizations are
            working on AI accelerator and semiconductor
            technologies.
            """,
        },
    ]

    print("=" * 60)
    print("RAG TEST")
    print("=" * 60)

    indexed = index_research(
        fetched_content=research,
        research_id=research_id,
    )

    print(f"\nResearch ID: {research_id}")
    print(f"Indexed chunks: {indexed}")

    question = (
        "What is India doing to develop "
        "its semiconductor industry?"
    )

    print(f"\nQuestion: {question}")

    result = answer_followup(
        question=question,
        research_id=research_id,
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nCONFIDENCE:")
    print(result["confidence"])

    print("\nINSUFFICIENT INFORMATION:")
    print(result["insufficient_information"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['title']}"
        )
        print(
            f"  {source['url']}"
        )

    print("\n" + "=" * 60)
    print("RAG TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()