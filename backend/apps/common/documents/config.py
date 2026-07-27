"""
Document configuration models for DatavionOS.

Provides immutable configuration objects used by the document
framework.

The configuration layer controls document behaviour without
coupling to storage providers or AI processing systems.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.documents.constants import (
    DEFAULT_ACCESS_LEVEL,
    DEFAULT_CATEGORY,
    DEFAULT_STATUS,
    DEFAULT_STORAGE_BACKEND,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentConfiguration:
    """
    Document framework configuration.

    Controls general document behaviour.
    """

    enabled: bool = True

    default_status: str = DEFAULT_STATUS

    default_category: str = DEFAULT_CATEGORY

    default_access_level: str = DEFAULT_ACCESS_LEVEL

    tenant_isolation: bool = True

    versioning_enabled: bool = True

    audit_enabled: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentStorageConfiguration:
    """
    Document storage configuration.

    Controls file storage behaviour.
    """

    backend: str = DEFAULT_STORAGE_BACKEND

    max_file_size_mb: int = 50

    allowed_file_types: tuple[str, ...] = (
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "docx",
        "xlsx",
    )

    encryption_enabled: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentAIConfiguration:
    """
    AI document processing configuration.

    Supports future:

    - OCR
    - document classification
    - embeddings
    - RAG ingestion
    """

    enabled: bool = True

    ocr_enabled: bool = True

    extraction_enabled: bool = True

    embedding_enabled: bool = True

    indexing_enabled: bool = True


DEFAULT_DOCUMENT_CONFIGURATION = DocumentConfiguration()


DEFAULT_DOCUMENT_STORAGE_CONFIGURATION = DocumentStorageConfiguration()


DEFAULT_DOCUMENT_AI_CONFIGURATION = DocumentAIConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_DOCUMENT_AI_CONFIGURATION",
    "DEFAULT_DOCUMENT_CONFIGURATION",
    "DEFAULT_DOCUMENT_STORAGE_CONFIGURATION",
    "DocumentAIConfiguration",
    "DocumentConfiguration",
    "DocumentStorageConfiguration",
)
