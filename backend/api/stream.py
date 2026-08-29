import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from ..services.research_event import research_events
from ..services.research_store import get_research_session
from .auth import get_current_user


router = APIRouter(
    prefix="/api/research",
    tags=["research-stream"],
)


NODE_LABELS = {
    "initialize_research": "Initializing research",
    "plan_research": "Planning research",
    "execute_research": "Searching the web",
    "fetch_content": "Reading sources",
    "check_completeness": "Checking research",
    "extract_claims": "Extracting evidence",
    "synthesise": "Building report",
    "index_research": "Indexing research",
}


def format_event(
    event: dict,
) -> str:

    event_type = event.get(
        "type",
        "message",
    )

    if event_type == "node_completed":

        node = event.get(
            "node",
            "unknown",
        )

        event = {
            **event,
            "label": NODE_LABELS.get(
                node,
                node,
            ),
        }

    return (
        f"event: {event_type}\n"
        f"data: {json.dumps(event)}\n\n"
    )


async def event_stream(
    research_id: str,
    session: dict,
) -> AsyncGenerator[str, None]:

    # 1. Yield initial connection event
    yield (
        "event: connected\n"
        f"data: {json.dumps({'research_id': research_id})}\n\n"
    )

    # 2. If the database already says it's completed/failed, yield that and end immediately.
    # This guarantees consistency even if the memory queue is lost (e.g. server restart).
    if session["status"] == "completed":
        yield format_event({
            "type": "research_completed",
            "report": session.get("report")
        })
        return
    elif session["status"] == "failed":
        yield format_event({
            "type": "research_failed",
            "error": session.get("error", "Unknown error")
        })
        return

    # 3. Otherwise, subscribe to the live in-memory event stream
    history = await research_events.get_history(research_id)
    pubsub = await research_events.subscribe(research_id)

    try:
        for event in history:
            yield format_event(event)
            if event.get("type") in {"research_completed", "research_failed"}:
                return

        while True:
            # get_message returns None if timeout is reached
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, 
                timeout=15.0
            )

            if message is None:
                yield ": heartbeat\n\n"
                continue

            event = json.loads(message["data"])
            yield format_event(event)

            if event.get("type") in {"research_completed", "research_failed"}:
                break

    finally:
        await pubsub.unsubscribe()
        await pubsub.close()


@router.get("/{research_id}/stream")
async def stream_research(
    research_id: str,
    user_id: str = Depends(get_current_user),
) -> StreamingResponse:
    session = await get_research_session(
        research_id=research_id,
        user_id=user_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Research session not found.",
        )

    return StreamingResponse(
        event_stream(research_id, session),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )