import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from .store import search_research


load_dotenv()


# ============================================================
# Configuration
# ============================================================

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

DEFAULT_TOP_K = 6
MAX_CONTEXT_CHARS = 30_000


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0,
    google_api_key=os.getenv(
        "GEMINI_API_KEY"
    ),
)


# ============================================================
# Structured Follow-up Response
# ============================================================

class FollowUpSource(BaseModel):

    title: str = Field(
        description="Title of the source."
    )

    url: str = Field(
        description="URL of the source."
    )


class FollowUpResponse(BaseModel):

    answer: str = Field(
        description=(
            "Answer to the user's follow-up "
            "question using only the provided context."
        )
    )

    confidence: str = Field(
        description=(
            "Confidence level: high, medium, or low."
        )
    )

    insufficient_information: bool = Field(
        description=(
            "True when the retrieved research "
            "does not contain enough information."
        )
    )

    sources: list[FollowUpSource] = Field(
        description=(
            "Sources used to answer the question."
        )
    )


followup_llm = llm.with_structured_output(
    FollowUpResponse
)


# ============================================================
# Context Builder
# ============================================================

def build_context(
    documents: list[Any],
) -> tuple[str, list[dict[str, str]]]:

    context_parts: list[str] = []
    sources: list[dict[str, str]] = []

    total_chars = 0

    for index, document in enumerate(
        documents,
        start=1,
    ):

        title = document.metadata.get(
            "source_title",
            "Untitled source",
        )

        url = document.metadata.get(
            "source_url",
            "",
        )

        content = document.page_content.strip()

        if not content:
            continue

        remaining = (
            MAX_CONTEXT_CHARS
            - total_chars
        )

        if remaining <= 0:
            break

        content = content[:remaining]

        context_parts.append(
            f"""
SOURCE {index}

TITLE:
{title}

URL:
{url}

CONTENT:
{content}
"""
        )

        total_chars += len(content)

        if url:

            sources.append(
                {
                    "title": title,
                    "url": url,
                }
            )

    return (
        "\n\n".join(context_parts),
        sources,
    )


# ============================================================
# Follow-up Answer
# ============================================================

def answer_followup(
    question: str,
    top_k: int = DEFAULT_TOP_K,
) -> dict[str, Any]:

    question = question.strip()

    if not question:

        raise ValueError(
            "Follow-up question cannot be empty."
        )

    # --------------------------------------------------------
    # Retrieve relevant research
    # --------------------------------------------------------

    documents = search_research(
        query=question,
        k=top_k,
    )

    if not documents:

        return {
            "answer": (
                "I couldn't find relevant "
                "information in the research."
            ),
            "confidence": "low",
            "insufficient_information": True,
            "sources": [],
        }

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context, retrieved_sources = (
        build_context(documents)
    )

    if not context:

        return {
            "answer": (
                "The research database did not "
                "contain usable content for this question."
            ),
            "confidence": "low",
            "insufficient_information": True,
            "sources": [],
        }

    # --------------------------------------------------------
    # Grounded prompt
    # --------------------------------------------------------

    prompt = f"""
You are Aria's follow-up research assistant.

The user has already completed a research session.

Answer the follow-up question using ONLY the
retrieved research context.

USER QUESTION:
{question}

RETRIEVED RESEARCH:
{context}

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent facts.
3. Do not infer unsupported facts.
4. Every factual statement must be supported
   by the retrieved research.
5. If the retrieved research is insufficient,
   explicitly say that the available research
   does not contain enough information.
6. Prefer precise answers over long answers.
7. Use the provided source information.
8. Set confidence to:
   - high when multiple relevant sources support
     the answer.
   - medium when the answer is supported but
     evidence is limited.
   - low when evidence is weak or incomplete.
9. Only include sources actually used to answer
   the question.
"""

    # --------------------------------------------------------
    # Generate structured answer
    # --------------------------------------------------------

    response = followup_llm.invoke(
        prompt
    )

    # --------------------------------------------------------
    # Return API-friendly response
    # --------------------------------------------------------

    return {
        "answer": response.answer,
        "confidence": response.confidence,
        "insufficient_information": (
            response.insufficient_information
        ),
        "sources": [
            source.model_dump()
            for source in response.sources
        ],
    }