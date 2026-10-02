"""
DatavionOS Search Indexer.

Enterprise document ingestion pipeline.

Flow:

Document
    |
    v
Chunking
    |
    v
EmbeddingService
    |
    v
VectorDocument
    |
    v
VectorEngine.index()


Supports:

- Clinical notes
- Laboratory reports
- FHIR resources
- Audit events
- Knowledge documents
- RAG ingestion
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.common.search.embeddings import (
    embedding_service,
)
from apps.common.search.vector import (
    vector_engine,
)
from apps.common.search.vector.types import (
    VectorDocument,
)

DEFAULT_CHUNK_SIZE = 1000


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentChunk:
    """
    Represents a searchable document chunk.
    """

    id: str

    content: str

    metadata: dict[str, Any] | None = None


class DocumentIndexer:
    """
    Enterprise document indexing service.
    """

    def chunk_document(
        self,
        *,
        document_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> list[DocumentChunk]:
        """
        Split document into searchable chunks.
        """

        chunks: list[DocumentChunk] = []

        for index in range(
            0,
            len(content),
            chunk_size,
        ):
            chunks.append(
                DocumentChunk(
                    id=f"{document_id}-{index}",
                    content=content[index : index + chunk_size],
                    metadata=metadata,
                )
            )

        return chunks

    def index_document(
        self,
        *,
        document_id: str,
        content: str,
        provider: str = "pgvector",
        embedding_provider: str = "local",
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """
        Index complete document.

        Returns number of indexed chunks.
        """

        chunks = self.chunk_document(
            document_id=document_id,
            content=content,
            metadata=metadata,
        )

        for chunk in chunks:
            vector = embedding_service.embed(
                text=chunk.content,
                provider=embedding_provider,
            )

            vector_document = VectorDocument(
                id=chunk.id,
                content=chunk.content,
                vector=vector,
                metadata=chunk.metadata,
            )

            vector_engine.index(
                document=vector_document,
                provider=provider,
            )

        return len(chunks)


document_indexer = DocumentIndexer()


__all__: tuple[str, ...] = (
    "DocumentChunk",
    "DocumentIndexer",
    "document_indexer",
)
