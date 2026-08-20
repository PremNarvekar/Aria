import os
import httpx

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def tavily_search(query: str, max_results: int = 5):
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )

    return response.get("results", [])


async def fetch_page(url: str):
    try:
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "content": response.text,
            }

    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "content": "",
        }

        