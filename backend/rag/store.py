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
) -> list[Document]:

    documents = []

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
) -> Chroma:

    documents = build_documents(
        fetched_content
    )

    if not documents:
        raise ValueError(
            "No research content available."
        )

    vector_store = get_vector_store()

    vector_store.add_documents(
        documents
    )

    return vector_store


def search_research(
    query: str,
    k: int = 5,
) -> list[Document]:

    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query,
        k=k,
    )