import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from .state import AgentState
from .tools import tavily_search, fetch_page

from ..models import ResearchReport

from ..rag.store import index_research as index_research_document
from ..rag.session import create_research_id


# ============================================================
# Configuration
# ============================================================

load_dotenv()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

MAX_SEARCH_QUERIES = 5
MAX_RESULTS_PER_QUERY = 5

DEFAULT_MAX_ITERATIONS = 5
DEFAULT_MAX_SOURCES = 20

MAX_CONTENT_PER_SOURCE = 12_000

FETCH_CONCURRENCY = 8
SEARCH_CONCURRENCY = 5

MAX_CLAIMS_PER_SOURCE = 10
MAX_CLAIM_CONTENT = 10_000
CLAIM_CONCURRENCY = 5


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

report_llm = llm.with_structured_output(
    ResearchReport 
)

# ============================================================
# Structured Outputs
# ============================================================

class SearchPlan(BaseModel):
    queries: list[str] = Field(
        description=(
            "A list of distinct search queries that investigate "
            "different aspects of the user's research question."
        )
    )


class CompletenessDecision(BaseModel):
    complete: bool = Field(
        description=(
            "Whether the available research is sufficient "
            "to answer the user's question."
        )
    )

    reason: str = Field(
        description=(
            "Short explanation of why the research is "
            "complete or incomplete."
        )
    )

    missing_aspects: list[str] = Field(
        default_factory=list,
        description=(
            "Important aspects that are still missing "
            "from the research."
        ),
    )


planner_llm = llm.with_structured_output(SearchPlan)

completeness_llm = llm.with_structured_output(
    CompletenessDecision
)

class Claim(BaseModel):
    
    statement: str =Field(
        description=(
            "A factual statement directly support"
            "by the provided source"
        )
    )
    
    evidence:str = Field(
        description=(
            "A short excerpt or precise evidence from "
            "the source supporting the claim"
        )
    )
    
    claim_type:str = Field(
        description=(
            "Category of the claim such as policy "
            "market, company , technology, financial",
            "competition or other"
        )
    )
    
class SourceClaims(BaseModel):
    claims: list[Claim]= Field(
        description=(
            "Factual claims extracted only from the"
            "provided source. "
        )
    )
    
claims_llm = llm.with_structured_output(
    SourceClaims
)

# ============================================================
# Helper: Normalize Query
# ============================================================

def normalize_query(query: str) -> str:
    """
    Normalize a search query so we can detect duplicates.
    """

    return " ".join(
        query.strip().lower().split()
    )


# ============================================================
# Helper: Normalize URL
# ============================================================

def normalize_url(url: str) -> str:
    """
    Normalize URLs for basic duplicate detection.
    """

    return url.strip().rstrip("/")


# ============================================================
# Helper: Build Research Context
# ============================================================

def build_research_context(
    fetched_content: list[dict[str, Any]],
) -> str:

    if not fetched_content:
        return "No research content has been collected yet."

    sources = []

    for index, item in enumerate(
        fetched_content,
        start=1,
    ):

        title = item.get(
            "title",
            "Untitled source",
        )

        url = item.get(
            "url",
            "",
        )

        content = item.get(
            "content",
            "",
        )

        content = content[
            :MAX_CONTENT_PER_SOURCE
        ]

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


# ============================================================
# Helper: Get Research Configuration
# ============================================================

def get_research_config(
    state: AgentState,
) -> tuple[int, int, int]:

    iteration = state.get(
        "research_iteration",
        0,
    )

    max_iterations = state.get(
        "max_iterations",
        DEFAULT_MAX_ITERATIONS,
    )

    max_sources = state.get(
        "max_sources",
        DEFAULT_MAX_SOURCES,
    )

    return (
        iteration,
        max_iterations,
        max_sources,
    )


# ============================================================
# Node 1 — Plan Research
# ============================================================

def plan_research(
    state: AgentState,
) -> dict[str, Any]:

    question = state["question"]

    previous_queries = state.get(
        "search_queries",
        [],
    )

    previous_queries_text = "\n".join(
        f"- {query}"
        for query in previous_queries
    )

    prompt = f"""
You are Aria's research planning agent.

User research question:

{question}

Previous searches already performed:

{previous_queries_text or "None"}

Generate up to {MAX_SEARCH_QUERIES} NEW search queries.

Requirements:

- Each query must investigate a different angle.
- Do not repeat previous queries.
- Do not produce minor variations of previous queries.
- Prioritize high-value information.
- Cover important missing aspects.
- Prefer primary or authoritative sources when appropriate.

Return only structured search queries.
"""

    plan = planner_llm.invoke(prompt)

    previous_normalized = {
        normalize_query(query)
        for query in previous_queries
    }

    new_queries = []

    for query in plan.queries:

        normalized = normalize_query(query)

        if not normalized:
            continue

        if normalized in previous_normalized:
            continue

        if normalized in {
            normalize_query(q)
            for q in new_queries
        }:
            continue

        new_queries.append(
            query.strip()
        )

        if len(new_queries) >= MAX_SEARCH_QUERIES:
            break

    return {
        "search_queries": new_queries,
    }


# ============================================================
# Node 2 — Execute Research
# ============================================================

async def execute_single_search(
    query: str,
) -> list[dict[str, Any]]:

    try:

        results = await asyncio.to_thread(
            tavily_search,
            query=query,
            max_results=MAX_RESULTS_PER_QUERY,
        )

        return [
            {
                "query": query,
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
                "score": result.get("score"),
            }
            for result in results
        ]

    except Exception:

        return []


async def execute_research(
    state: AgentState,
) -> dict[str, Any]:

    queries = state.get(
        "search_queries",
        [],
    )

    existing_results = state.get(
        "search_results",
        [],
    )

    existing_urls = {
        normalize_url(
            result.get("url", "")
        )
        for result in existing_results
        if result.get("url")
    }

    semaphore = asyncio.Semaphore(
        SEARCH_CONCURRENCY
    )

    async def limited_search(query: str):

        async with semaphore:
            return await execute_single_search(
                query
            )

    results_by_query = await asyncio.gather(
        *[
            limited_search(query)
            for query in queries
        ]
    )

    new_results = []

    seen_urls = set(
        existing_urls
    )

    for results in results_by_query:

        for result in results:

            url = result.get("url")

            if not url:
                continue

            normalized_url = normalize_url(url)

            if normalized_url in seen_urls:
                continue

            seen_urls.add(
                normalized_url
            )

            new_results.append(
                result
            )

    return {
        "search_results": new_results,
    }


# ============================================================
# Node 3 — Fetch Content
# ============================================================

async def fetch_single_page(
    result: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:

    url = result.get("url")

    if not url:
        return None, None

    try:

        page = await fetch_page(url)

        content = page.get(
            "content",
            "",
        )

        if not content:
            return (
                None,
                {
                    "url": url,
                    "reason": "empty_content",
                },
            )

        return (
            {
                "url": url,
                "title": result.get("title"),
                "content": content,
                "query": result.get("query"),
                "score": result.get("score"),
            },
            None,
        )

    except Exception as exc:

        return (
            None,
            {
                "url": url,
                "reason": str(exc),
            },
        )


async def fetch_content(
    state: AgentState,
) -> dict[str, Any]:

    results = state.get(
        "search_results",
        [],
    )

    existing_content = state.get(
        "fetched_content",
        [],
    )

    existing_urls = {
        normalize_url(
            item.get("url", "")
        )
        for item in existing_content
        if item.get("url")
    }

    results_to_fetch = [
        result
        for result in results
        if result.get("url")
        and normalize_url(
            result["url"]
        ) not in existing_urls
    ]

    semaphore = asyncio.Semaphore(
        FETCH_CONCURRENCY
    )

    async def limited_fetch(result):

        async with semaphore:
            return await fetch_single_page(
                result
            )

    responses = await asyncio.gather(
        *[
            limited_fetch(result)
            for result in results_to_fetch
        ]
    )

    fetched = []
    failures = []

    for content, failure in responses:

        if content:
            fetched.append(content)

        if failure:
            failures.append(failure)

    return {
        "fetched_content": fetched,
        "failed_fetches": failures,
    }


# ============================================================
# Node 4 — Check Completeness
# ============================================================

def check_completeness(
    state: AgentState,
    ) -> dict[str, Any]:

    question = state["question"]

    fetched_content = state.get(
        "fetched_content",
        [],
    )

    iteration, max_iterations, max_sources = (
        get_research_config(state)
    )

    research_context = build_research_context(
        fetched_content
    )

    prompt = f"""
You are Aria's research completeness evaluator.

Original question:

{question}

Research collected:

{research_context}

Determine whether the collected research is sufficient
to answer the original question accurately and
comprehensively.

Evaluate:

1. Relevance
2. Coverage
3. Source quality
4. Source diversity
5. Evidence quality
6. Missing important aspects

Return complete=true only when the available research
is genuinely sufficient.

If important information is missing:

- return complete=false
- identify the missing aspects

Do not judge completeness based only on the number
of sources.
"""

    decision = completeness_llm.invoke(
        prompt
    )

    current_source_count = len(
        fetched_content
    )

    reached_iteration_limit = (
        iteration >= max_iterations
    )

    reached_source_limit = (
        current_source_count >= max_sources
    )

    if decision.complete:
        
        research_complete = True
        research_terminated = True
        termination_reason = "research_complete"
        
    elif reached_iteration_limit:
        research_complete = False
        research_terminated = True 
        termination_reason = "max_iterations"
        
    elif reached_source_limit:
        research_complete = False
        research_terminated = True 
        termination_reason = "max_sources"
        
    else : 
        research_complete = False 
        research_terminated = False
        termination_reason = "more_research_needed"
        
    return {
        "research_complete": research_complete,
        "completeness_reason": decision.reason,
        "missing_aspects":decision.missing_aspects,
        "research_iteration":iteration + 1,
        "research_terminated":research_terminated,
        "termination_reason":termination_reason
        
    }
        

async def extract_claims_from_source(
    source: dict[str, Any],
) -> list[dict[str, Any]]:

    title = source.get(
        "title",
        "Untitled source",
    )

    url = source.get(
        "url",
        "",
    )

    content = source.get(
        "content",
        "",
    )[:MAX_CLAIM_CONTENT]

    if not content:
        return []

    prompt = f"""
You are Aria's evidence extraction agent.

Extract factual claims supported ONLY by this source.

SOURCE TITLE:
{title}

SOURCE URL:
{url}

SOURCE CONTENT:
{content}

Rules:

1. Extract only claims supported by this source.
2. Do not invent information.
3. Do not combine information from other sources.
4. Do not make assumptions.
5. Each claim must be independently understandable.
6. Include concise evidence supporting each claim.
7. Prefer specific factual claims over vague statements.
8. Do not extract opinions unless clearly identified.
9. Ignore navigation, advertisements, cookie notices,
   and unrelated page content.

Return structured claims only.
"""

    try:
        result = await asyncio.to_thread(
            claims_llm.invoke,
            prompt,
        )

        claims = result.claims[
            :MAX_CLAIMS_PER_SOURCE
        ]

        return [
            {
                "statement": claim.statement,
                "evidence": claim.evidence,
                "claim_type": claim.claim_type,
                "source_url": url,
                "source_title": title,
            }
            for claim in claims
        ]

    except Exception as exc:
        print(
            f"Claim extraction failed for {url}: {exc}"
        )
        return []


async def extract_claims(
    state: AgentState,
) -> dict[str, Any]:

    fetched_content = state.get(
        "fetched_content",
        [],
    )

    if not fetched_content:
        return {
            "claims": [],
        }

    semaphore = asyncio.Semaphore(
        CLAIM_CONCURRENCY
    )

    async def limited_extraction(
        source: dict[str, Any],
    ) -> list[dict[str, Any]]:

        async with semaphore:
            return await extract_claims_from_source(
                source
            )

    results = await asyncio.gather(
        *[
            limited_extraction(source)
            for source in fetched_content
        ]
    )

    claims: list[dict[str, Any]] = []

    for source_claims in results:
        claims.extend(source_claims)

    return {
        "claims": claims,
    }
def synthesise(
    state: AgentState,
) -> dict[str, Any]:
    
    question = state['question']
    
    claims = state.get(
        "claims",
        [],
    )
    
    if not claims:
        return{
            "report":None,
        }
        
    evidence = "\n\n".join(
    f"""
CLAIM:
{claim.get("statement", "")}

EVIDENCE:
{claim.get("evidence", "")}

SOURCE:
{claim.get("source_title", "")}

URL:
{claim.get("source_url", "")}

"""
        for claim in claims 
    )
    prompt = f"""
You are Aria's research synthesis agent.

USER QUESTION:
{question}

EXTRACTED EVIDENCE:
{evidence}

Create a research report answering the user's
question using ONLY the supplied evidence.

Rules:

1. Do not invent facts.
2. Do not introduce information not present
   in the supplied claims.
3. Every important factual finding must be
   supported by the supplied evidence.
4. Keep the analysis directly relevant to
   the user's question.
5. Preserve source attribution.
6. If the evidence is insufficient, say so.
"""
    report = report_llm.invoke(
        prompt
    )
    return {
        "report":report.model_dump()
    }


def index_research(
    state: AgentState
) -> dict[str, Any]:
    
    fetched_content = state.get(
        "fetched_content",
        "",
    )
    
    research_id = state.get(
        "research_id",
        "",
    )
    
    if not research_id:
        raise ValueError(
            "research_id is required before indexing research. "
        )
        
    if not fetched_content:
        return {
            "indexed_chunks":0,
            "rag_indexed": False,
        }
        
    indexed_chunks = index_research_documents(
        fetched_content=fetched_content,
        research_id= research_id,
    
    )
    
    return {
        "indexed_chunks":indexed_chunks,
        "rag_indexed":True
    }
    
def initialize_research(
    state: AgentState,
) -> dict[str, Any]:

    research_id = state.get("research_id")

    if research_id:
        return {
            "research_id": research_id,
        }

    return {
        "research_id": create_research_id(),
    }