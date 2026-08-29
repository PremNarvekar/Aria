import asyncio
import json
import redis.asyncio as redis
from typing import Any
import os

# Assuming Redis is running on localhost or a service named "redis" in Docker
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

class ResearchEventManager:
    def __init__(self):
        self.redis_client = redis.from_url(REDIS_URL)

    async def subscribe(self, research_id: str):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"research:events:{research_id}")
        return pubsub

    async def get_history(self, research_id: str) -> list[dict[str, Any]]:
        events_json = await self.redis_client.lrange(f"research:history:{research_id}", 0, -1)
        return [json.loads(e) for e in events_json]

    async def publish(self, research_id: str, event: dict[str, Any]) -> None:
        event_str = json.dumps(event)
        
        # Save to history list
        await self.redis_client.rpush(f"research:history:{research_id}", event_str)
        # Set expiry for cleanup (e.g., 24 hours)
        await self.redis_client.expire(f"research:history:{research_id}", 86400)
        
        # Publish to live subscribers
        await self.redis_client.publish(f"research:events:{research_id}", event_str)

research_events = ResearchEventManager()