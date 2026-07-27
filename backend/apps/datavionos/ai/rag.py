"""
Retrieval-Augmented Generation (RAG) contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.ai.chat import (
    ChatResponse,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RAGDocument:
    """
    Immutable retrieved document.
    """

    identifier: str

    content: str

    score: float

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class RAGRequest:
    """
    Immutable retrieval-augmented generation request.
    """

    query: str

    limit: int = 5

    namespace: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class RAGResponse:
    """
    Immutable retrieval-augmented generation response.
    """

    response: ChatResponse

    documents: tuple[RAGDocument, ...]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class RAGEngine(
    Protocol,
):
    """
    Retrieval-Augmented Generation engine.
    """

    async def generate(
        self,
        request: RAGRequest,
    ) -> RAGResponse:
        """
        Execute a retrieval-augmented generation workflow.
        """


__all__ = [
    "RAGDocument",
    "RAGEngine",
    "RAGRequest",
    "RAGResponse",
]
