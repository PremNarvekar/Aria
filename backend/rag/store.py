import os
from typing import Any

import chromadb
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .embeddings import embeddings


load_dotenv()


CHROMA_API_KEY = os.getenv(
    "CHROMA_API_KEY"
)

CHROMA_TENANT = os.getenv(
    "CHROMA_TENANT"
)

CHROMA_DATABASE = os.getenv(
    "CHROMA_DATABASE"
)

COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION",
    "aria_research",
)


chroma_client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE,
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
)


def build_documents(
    fetched_content: list[dict[str, Any]],
    research_id:str
) -> list[Document]:

    documents: list[Document] = []

    for source in fetched_content:

        content = source.get(
            "content",
            "",
        )

        if not content:
            continue

        chunks = text_splitter.split_text(
            content
        )

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "research_id":research_id,
                        "source_url": source.get(
                            "url",
                            "",
                        ),
                        "source_title": source.get(
                            "title",
                            "",
                        ),
                        "query": source.get(
                            "query",
                            "",
                        ),
                    },
                )
            )

    return documents


def get_vector_store() -> Chroma:

    return Chroma(
        client=chroma_client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )


def index_research(
    fetched_content: list[dict[str, Any]],
    research_id: str
) -> int:

    documents = build_documents(
        fetched_content=fetched_content,
        research_id= research_id
    )

    if not documents:
        raise ValueError(
            "No research content available."
        )

    vector_store = get_vector_store()

    vector_store.add_documents(
        documents
    )

    return len(documents)


def search_research(
    query: str,
    research_id:str,
    k: int = 5,
) -> list[Document]:
    
    if not research_id:
        raise ValueError(
            "research_id is required for research retrieval. "
        )

    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query=query,
        k=k,
        filter={
            "research_id":research_id
        }
    )