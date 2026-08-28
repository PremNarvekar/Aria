import asyncio
from collections import defaultdict
from typing import Any


class ResearchEventManager:

    def __init__(self) -> None:
        self._subscribers: dict[
            str,
            set[asyncio.Queue[dict[str, Any]]],
        ] = defaultdict(set)

    def subscribe(
        self,
        research_id: str,
    ) -> asyncio.Queue[dict[str, Any]]:

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        self._subscribers[research_id].add(queue)

        return queue

    def unsubscribe(
        self,
        research_id: str,
        queue: asyncio.Queue[dict[str, Any]],
    ) -> None:

        subscribers = self._subscribers.get(research_id)

        if not subscribers:
            return

        subscribers.discard(queue)

        if not subscribers:
            self._subscribers.pop(
                research_id,
                None,
            )

    async def publish(
        self,
        research_id: str,
        event: dict[str, Any],
    ) -> None:

        subscribers = self._subscribers.get(
            research_id,
            set(),
        )

        if not subscribers:
            return

        await asyncio.gather(
            *[
                queue.put(event)
                for queue in subscribers
            ]
        )


research_events = ResearchEventManager()