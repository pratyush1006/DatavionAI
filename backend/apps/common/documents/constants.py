"""
Document constants for DatavionOS.

Defines framework-wide constants for document lifecycle,
storage backends, access control, and processing states.
"""

from __future__ import annotations

###############################################################################
# Document Lifecycle States
###############################################################################

STATUS_DRAFT = "draft"

STATUS_ACTIVE = "active"

STATUS_ARCHIVED = "archived"

STATUS_DELETED = "deleted"


###############################################################################
# Document Categories
###############################################################################

CATEGORY_GENERAL = "general"

CATEGORY_MEDICAL = "medical"

CATEGORY_CLINICAL = "clinical"

CATEGORY_LABORATORY = "laboratory"

CATEGORY_FINANCIAL = "financial"

CATEGORY_LEGAL = "legal"

CATEGORY_SYSTEM = "system"


###############################################################################
# Storage Backends
###############################################################################

STORAGE_LOCAL = "local"

STORAGE_S3 = "s3"

STORAGE_AZURE = "azure"

STORAGE_GCP = "gcp"


###############################################################################
# Access Levels
###############################################################################

ACCESS_PRIVATE = "private"

ACCESS_INTERNAL = "internal"

ACCESS_SHARED = "shared"

ACCESS_PUBLIC = "public"


###############################################################################
# Document Processing States
###############################################################################

PROCESSING_PENDING = "pending"

PROCESSING_PROCESSING = "processing"

PROCESSING_COMPLETED = "completed"

PROCESSING_FAILED = "failed"


###############################################################################
# Version Operations
###############################################################################

VERSION_CREATE = "create"

VERSION_UPDATE = "update"

VERSION_RESTORE = "restore"


###############################################################################
# Default Values
###############################################################################

DEFAULT_STATUS = STATUS_DRAFT

DEFAULT_CATEGORY = CATEGORY_GENERAL

DEFAULT_STORAGE_BACKEND = STORAGE_LOCAL

DEFAULT_ACCESS_LEVEL = ACCESS_PRIVATE


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "ACCESS_INTERNAL",
    "ACCESS_PRIVATE",
    "ACCESS_PUBLIC",
    "ACCESS_SHARED",
    "CATEGORY_CLINICAL",
    "CATEGORY_FINANCIAL",
    "CATEGORY_GENERAL",
    "CATEGORY_LABORATORY",
    "CATEGORY_LEGAL",
    "CATEGORY_MEDICAL",
    "CATEGORY_SYSTEM",
    "DEFAULT_ACCESS_LEVEL",
    "DEFAULT_CATEGORY",
    "DEFAULT_STATUS",
    "DEFAULT_STORAGE_BACKEND",
    "PROCESSING_COMPLETED",
    "PROCESSING_FAILED",
    "PROCESSING_PENDING",
    "PROCESSING_PROCESSING",
    "STATUS_ACTIVE",
    "STATUS_ARCHIVED",
    "STATUS_DELETED",
    "STATUS_DRAFT",
    "STORAGE_AZURE",
    "STORAGE_GCP",
    "STORAGE_LOCAL",
    "STORAGE_S3",
    "VERSION_CREATE",
    "VERSION_RESTORE",
    "VERSION_UPDATE",
)
