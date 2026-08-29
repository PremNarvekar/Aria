"""
End-to-end test for the PostgreSQL research store.

Creates the table, inserts a row, reads it, updates it,
reads again, and prints each step.

Run from project root:
    backend\\.venv\\Scripts\\python -m backend.services.test_store
"""

import asyncio

from dotenv import load_dotenv

load_dotenv()

from backend.db.database import engine, Base
from backend.db.models import ResearchSession  # noqa: F401
from backend.services.research_store import (
    create_research_session,
    get_research_session,
    update_research_session,
)


async def main() -> None:

    # Step 1: Create the table if it doesn't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] Table created (or already exists)\n")

    # Step 2: Create a research session
    session = await create_research_session(
        "What is NVIDIA's AI strategy in 2025?"
    )
    print("[OK] Created session:")
    print(f"  research_id: {session['research_id']}")
    print(f"  status:      {session['status']}")
    print(f"  question:    {session['question']}")
    print(f"  created_at:  {session['created_at']}")
    print()

    # Step 3: Read it back
    fetched = await get_research_session(session["research_id"])
    assert fetched is not None, "Session should exist"
    assert fetched["research_id"] == session["research_id"]
    assert fetched["status"] == "queued"
    print("[OK] Fetched session -- status is 'queued'\n")

    # Step 4: Update status to running
    updated = await update_research_session(
        session["research_id"],
        status="running",
    )
    assert updated is not None
    assert updated["status"] == "running"
    print("[OK] Updated status to 'running'")
    print(f"  updated_at:  {updated['updated_at']}\n")

    # Step 5: Update to completed with a report
    completed = await update_research_session(
        session["research_id"],
        status="completed",
        report={
            "executive_summary": "NVIDIA dominates AI infrastructure.",
            "key_finding": ["H100 demand exceeds supply"],
            "analysis": "Strong competitive moat.",
            "sources": [{"title": "NVIDIA 10-K", "url": "https://nvidia.com"}],
        },
    )
    assert completed is not None
    assert completed["status"] == "completed"
    assert completed["report"] is not None
    print("[OK] Updated to 'completed' with report")
    print(f"  report keys: {list(completed['report'].keys())}\n")

    # Step 6: Verify non-existent session returns None
    ghost = await get_research_session("does-not-exist")
    assert ghost is None
    print("[OK] Non-existent session returns None\n")

    print("=" * 50)
    print("  ALL TESTS PASSED -- PostgreSQL store is working")
    print("=" * 50)

    # Cleanup: dispose the engine
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
