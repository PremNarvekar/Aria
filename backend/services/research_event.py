"""
In-memory research event manager for local development (no Redis required).
In production (Docker), swap this for the Redis Pub/Sub version.
"""

import asyncio
import json
from collections import defaultdict, deque
from typing import Any


class ResearchEventManager:

    def __init__(self, max_history: int = 200) -> None:
        self._subscribers: dict[str, set[asyncio.Queue[dict[str, Any]]]] = defaultdict(set)
        self._history: dict[str, deque[dict[str, Any]]] = defaultdict(lambda: deque(maxlen=max_history))

    async def subscribe(self, research_id: str) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self._subscribers[research_id].add(queue)
        return queue

    async def unsubscribe(self, research_id: str, queue: asyncio.Queue[dict[str, Any]]) -> None:
        subs = self._subscribers.get(research_id)
        if subs:
            subs.discard(queue)
            if not subs:
                self._subscribers.pop(research_id, None)

    async def get_history(self, research_id: str) -> list[dict[str, Any]]:
        return list(self._history.get(research_id, []))

    async def publish(self, research_id: str, event: dict[str, Any]) -> None:
        self._history[research_id].append(event)
        for queue in self._subscribers.get(research_id, set()):
            await queue.put(event)


research_events = ResearchEventManager()