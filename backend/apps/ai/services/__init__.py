"""AI application services."""

from __future__ import annotations

from .chat import generate
from .prompts import render
from .rag import add_text_document, chunk_text, index_document, retrieve
from .registry import ensure_department_applications

__all__ = (
    "generate",
    "render",
    "add_text_document",
    "chunk_text",
    "index_document",
    "retrieve",
    "ensure_department_applications",
)

from .reliability import (
    CircuitOpenError,
    acquire_idempotency_lock,
    complete_with_reliability,
    release_idempotency_lock,
    request_fingerprint,
)
