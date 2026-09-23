from typing import Any

from langchain_groq import ChatGroq

from .store import get_vector_store
import os


class FollowUpService:

    def __init__(self) -> None:
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant", # using smaller model for fast RAG chat
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    async def answer(
        self,
        research_id: str,
        question: str,
        k: int = 5,
    ) -> dict[str, Any]:

        vector_store = get_vector_store()

        documents = await vector_store.asimilarity_search(
            question,
            k=k,
            filter={
                "research_id": research_id,
            },
        )

        if not documents:
            return {
                "answer": (
                    "I couldn't find enough relevant "
                    "information in this research."
                ),
                "sources": [],
            }

        context_parts: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            context_parts.append(
                f"""
SOURCE {index}

Title:
{document.metadata.get("source_title", "Unknown")}

URL:
{document.metadata.get("source_url", "")}

Content:
{document.page_content}
"""
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are Aria's follow-up research assistant.

Answer the user's question using ONLY the research
context provided below.

RESEARCH ID:
{research_id}

USER QUESTION:
{question}

RESEARCH CONTEXT:
{context}

Rules:

1. Use only information supported by the research context.
2. Do not invent facts.
3. If the context does not contain enough information,
   clearly say so.
4. Give a direct and useful answer.
5. Preserve important nuance.
6. Cite the relevant sources using their URLs.
"""

        response = await self.llm.ainvoke(prompt)

        sources = [
            {
                "title": document.metadata.get(
                    "source_title",
                    "Unknown",
                ),
                "url": document.metadata.get(
                    "source_url",
                    "",
                ),
            }
            for document in documents
        ]

        return {
            "answer": response.content,
            "sources": sources,
        }


followup_service = FollowUpService()