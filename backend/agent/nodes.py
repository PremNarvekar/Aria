import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from .state import AgentState
from .tools import tavily_search, fetch_page



# Configuration


load_dotenv()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

MAX_SEARCH_QUERIES = 5
DEFAULT_MAX_ITERATIONS = 3
MAX_CONTENT_PER_SOURCE = 12_000



# LLM


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)



# Structured Outputs
class CompletenessDecision(BaseModel):
    complete: bool = Field(
        description=(
            "True when the collected research is sufficient "
            "to answer the user's question accurately."
        )
    )

    reason: str = Field(
        description=(
            "Brief explanation describing why the research "
            "is or is not sufficient."
        )
    )


completeness_llm = llm.with_structured_output(
    CompletenessDecision
)



# Helper Functions
def build_research_context(
    fetched_content: list[dict[str, Any]],
) -> str:
    """
    Convert fetched documents into a clean text context
    that can be passed to the LLM.
    """

    if not fetched_content:
        return "No research content has been collected yet."

    sources = []

    for index, item in enumerate(fetched_content, start=1):
        url = item.get("url", "")
        title = item.get("title", "Untitled source")
        content = item.get("content", "")

        content = content[:MAX_CONTENT_PER_SOURCE]

        sources.append(
            f"""
SOURCE {index}

Title:
{title}

URL:
{url}

Content:
{content}
"""
        )

    return "\n\n".join(sources)


def get_iteration_config(
    state: AgentState,
) -> tuple[int, int]:
    """
    Read the current research iteration and maximum
    allowed iterations from state.
    """

    iteration = state.get(
        "research_iteration",
        0,
    )

    max_iterations = state.get(
        "max_iterations",
        DEFAULT_MAX_ITERATIONS,
    )

    return iteration, max_iterations



# Node 1 — Plan Research

def plan_research(state: AgentState,) -> dict[str, Any]:

    question = state["question"]

    prompt = f"""
You are the research planning agent for Aria.

The user wants to research:

{question}

Generate {MAX_SEARCH_QUERIES} high-quality search queries.

Each query must investigate a DIFFERENT angle of the
user's question.

Avoid generating multiple queries that search for the
same information.

Think about useful angles such as:

- background
- current information
- technical details
- business or market information
- competitors
- recent developments
- primary sources

Return ONLY the search queries.

One query per line.
"""

    response = llm.invoke(prompt)

    queries = [
        line.strip()
        for line in response.content.splitlines()
        if line.strip()
    ]

    return {
        "search_queries": queries[:MAX_SEARCH_QUERIES],
    }



# Node 2 — Execute Research


def execute_research(
    state: AgentState,
) -> dict[str, Any]:

    queries = state.get(
        "search_queries",
        [],
    )

    all_results: list[dict[str, Any]] = []

    for query in queries:

        results = tavily_search(
            query=query,
            max_results=5,
        )

        for result in results:

            all_results.append(
                {
                    "query": query,
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "score": result.get("score"),
                }
            )

    return {
        "search_results": all_results,
    }



# Node 3 — Fetch Content


async def fetch_content(
    state: AgentState,
) -> dict[str, Any]:

    results = state.get(
        "search_results",
        [],
    )

    fetched: list[dict[str, Any]] = []

    for result in results:

        url = result.get("url")

        if not url:
            continue

        page = await fetch_page(url)

        if not page.get("content"):
            continue

        fetched.append(
            {
                "url": url,
                "title": result.get("title"),
                "content": page["content"],
                "query": result.get("query"),
                "score": result.get("score"),
            }
        )

    return {
        "fetched_content": fetched,
    }



# Node 4 — Check Completeness


def check_completeness(
    state: AgentState,
) -> dict[str, Any]:

    question = state["question"]

    fetched_content = state.get(
        "fetched_content",
        [],
    )

    iteration, max_iterations = get_iteration_config(
        state
    )

    research_context = build_research_context(
        fetched_content
    )

    prompt = f"""
You are Aria's research completeness evaluator.

Original user question:

{question}

Research collected so far:

{research_context}

Determine whether the collected research is sufficient
to answer the original question accurately and
comprehensively.

Evaluate:

1. Relevance
2. Coverage
3. Source quality
4. Missing important information
5. Evidence supporting the answer

Return complete=true ONLY if the available research
is sufficient.

If important information is still missing, return
complete=false.

Explain your decision briefly.
"""

    decision = completeness_llm.invoke(
        prompt
    )

    
    # Deterministic safety rule
    

    if decision.complete:
        is_complete = True

    elif iteration >= max_iterations:
        is_complete = True

    else:
        is_complete = False

    return {
        "is_complete": is_complete,
        "completeness_reason": decision.reason,
        "research_iteration": iteration + 1,
    }

def check_completeness(state: AgentState,) -> dict[str, Any]:

    question = state["question"]

    fetched_content = state.get(
        "fetched_content",
        [],
    )

    iteration, max_iterations = get_iteration_config(
        state
    )

    research_context = build_research_context(
        fetched_content
    )

    prompt = f"""
You are Aria's research completeness evaluator.

Original user question:

{question}

Research collected so far:

{research_context}

Determine whether the collected research is sufficient
to answer the original question accurately and comprehensively.

Evaluate:

1. Relevance
2. Coverage
3. Source quality
4. Missing important information
5. Evidence supporting the answer

Return complete=true ONLY if the available research
is sufficient.

If important information is still missing, return
complete=false.

Explain your decision briefly.
"""

    decision = completeness_llm.invoke(prompt)

    if decision.complete:
        is_complete = True

    elif iteration >= max_iterations:
        is_complete = True

    else:
        is_complete = False

    return {
        "is_complete": is_complete,
        "completeness_reason": decision.reason,
        "research_iteration": iteration + 1,
    }