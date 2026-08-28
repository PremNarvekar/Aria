import asyncio
from typing import Any

from ..agent.graph import research_graph
from ..services.research_events import research_events
from ..services.research_store import update_research_session


async def run_research(
    research_id: str,
    question: str,
) -> None:

    update_research_session(
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

        update_research_session(
            research_id,
            status="completed",
            report=final_state.get("report"),
            sources=final_state.get(
                "fetched_content",
                [],
            ),
            indexed_chunks=final_state.get(
                "indexed_chunks",
                0,
            ),
            rag_indexed=final_state.get(
                "rag_indexed",
                False,
            ),
        )

        await research_events.publish(
            research_id,
            {
                "type": "research_completed",
                "research_id": research_id,
            },
        )

    except asyncio.CancelledError:

        update_research_session(
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

    except Exception as exc:

        update_research_session(
            research_id,
            status="failed",
            error=str(exc),
        )

        await research_events.publish(
            research_id,
            {
                "type": "research_failed",
                "research_id": research_id,
                "error": str(exc),
            },
        )