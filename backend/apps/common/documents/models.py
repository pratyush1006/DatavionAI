"""
Document models for DatavionOS.

Defines immutable framework-level document objects.

These models describe document lifecycle and metadata only.

Business-specific document logic belongs to domain applications:

- patients
- laboratories
- billing
- clinical
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.documents.constants import (
    DEFAULT_ACCESS_LEVEL,
    DEFAULT_CATEGORY,
    DEFAULT_STATUS,
)
from apps.common.documents.types import (
    DocumentContext,
    DocumentID,
    DocumentMetadata,
    DocumentName,
    DocumentType,
    DocumentVersion,
    FileName,
    FilePath,
    MimeType,
    OrganizationID,
    StorageKey,
    TenantID,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentMetadataInfo:
    """
    Document metadata information.
    """

    file_name: FileName

    mime_type: MimeType

    file_size: int

    storage_key: StorageKey

    file_path: FilePath | None = None

    metadata: DocumentMetadata = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentVersionInfo:
    """
    Represents a document version.
    """

    version: DocumentVersion

    storage_key: StorageKey

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class Document:
    """
    Core document definition.

    Represents a stored platform document.
    """

    document_id: DocumentID

    name: DocumentName

    document_type: DocumentType

    metadata: DocumentMetadataInfo

    status: str = DEFAULT_STATUS

    category: str = DEFAULT_CATEGORY

    access_level: str = DEFAULT_ACCESS_LEVEL

    tenant_id: TenantID = None

    organization_id: OrganizationID = None

    versions: tuple[DocumentVersionInfo, ...] = ()

    context: DocumentContext = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentResult:
    """
    Result returned after document operations.
    """

    success: bool

    document_id: DocumentID

    message: str = ""

    metadata: DocumentMetadata = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "Document",
    "DocumentMetadataInfo",
    "DocumentResult",
    "DocumentVersionInfo",
)
