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

            # Clean HTML to plain text using BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            text_content = soup.get_text(separator=" ", strip=True)

            # Cap the maximum text returned per page for embedding to 10000 chars
            MAX_RAW_LENGTH = 10000
            if len(text_content) > MAX_RAW_LENGTH:
                text_content = text_content[:MAX_RAW_LENGTH] + "..."

            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "content": text_content,
            }

    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "content": "",
        }

        