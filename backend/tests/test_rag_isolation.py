from backend.rag.session import create_research_id
from backend.rag.store import index_research
from backend.rag.followup import answer_followup


def main():

    nvidia_id = create_research_id()
    apple_id = create_research_id()

    nvidia_research = [
        {
            "title": "NVIDIA AI Chips",
            "url": "https://example.com/nvidia",
            "query": "NVIDIA AI chips",
            "content": """
            NVIDIA develops GPUs and AI accelerators
            for artificial intelligence workloads.
            NVIDIA also develops the CUDA software ecosystem.
            """,
        }
    ]

    apple_research = [
        {
            "title": "Apple Silicon",
            "url": "https://example.com/apple",
            "query": "Apple silicon",
            "content": """
            Apple develops its own silicon chips for
            Macs, iPhones and iPads.
            Apple silicon integrates CPU and GPU
            capabilities into system-on-chip designs.
            """,
        }
    ]

    print("=" * 60)
    print("RAG ISOLATION TEST")
    print("=" * 60)

    print("\nIndexing NVIDIA...")
    nvidia_count = index_research(
        nvidia_research,
        nvidia_id,
    )

    print(f"NVIDIA chunks: {nvidia_count}")

    print("\nIndexing Apple...")
    apple_count = index_research(
        apple_research,
        apple_id,
    )

    print(f"Apple chunks: {apple_count}")

    print("\nNVIDIA FOLLOW-UP")

    result = answer_followup(
        question="What technology does the company develop?",
        research_id=nvidia_id,
    )

    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(f"- {source['title']}")

    print("\nAPPLE FOLLOW-UP")

    result = answer_followup(
        question="What technology does the company develop?",
        research_id=apple_id,
    )

    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(f"- {source['title']}")

    print("\n" + "=" * 60)
    print("ISOLATION TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()