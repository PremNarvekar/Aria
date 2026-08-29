import asyncio
from typing import Any
from backend.worker.celery_app import celery_app
from backend.agent.graph import research_graph
from backend.services.research_store import update_research_session
from backend.services.research_event import research_events


async def async_run_research(research_id: str, question: str) -> None:
    """The core asynchronous research workflow."""
    
    await update_research_session(
        research_id,
        status="running",
    )

    await research_events.publish(
        research_id,
        {
            "type": "research_started",
            "research_id": research_id,
        },
    )

    initial_state: dict[str, Any] = {
        "question": question,
        "research_id": research_id,
        "research_iteration": 0,
        "max_iterations": 5,
        "max_sources": 20,
        "search_queries": [],
        "search_results": [],
        "fetched_content": [],
        "failed_fetches": [],
        "claims": [],
    }

    final_state: dict[str, Any] = initial_state.copy()

    try:
        async for event in research_graph.astream(
            initial_state,
            stream_mode="updates",
        ):
            if not event:
                continue

            for node_name, state_update in event.items():
                if not isinstance(state_update, dict):
                    continue

                final_state.update(state_update)

                await research_events.publish(
                    research_id,
                    {
                        "type": "node_completed",
                        "research_id": research_id,
                        "node": node_name,
                    },
                )

        await update_research_session(
            research_id,
            status="completed",
            report=final_state.get("report"),
            sources=final_state.get("fetched_content", []),
            indexed_chunks=final_state.get("indexed_chunks", 0),
            rag_indexed=final_state.get("rag_indexed", False),
        )

        await research_events.publish(
            research_id,
            {
                "type": "research_completed",
                "research_id": research_id,
            },
        )

    except asyncio.CancelledError:
        await update_research_session(
            research_id,
            status="failed",
            error="Research task was cancelled.",
        )
        await research_events.publish(
            research_id,
            {
                "type": "research_failed",
                "research_id": research_id,
                "error": "Research task was cancelled.",
            },
        )
        raise

    except Exception as e:
        await update_research_session(
            research_id,
            status="failed",
            error=f"Research execution failed: {str(e)}",
        )
        await research_events.publish(
            research_id,
            {
                "type": "research_failed",
                "research_id": research_id,
                "error": "Research execution failed.",
            },
        )


@celery_app.task(name="backend.worker.tasks.execute_research_task")
def execute_research_task(research_id: str, question: str):
    """
    Synchronous Celery task wrapper that runs the async research loop.
    Celery workers call this function.
    """
    asyncio.run(async_run_research(research_id, question))
