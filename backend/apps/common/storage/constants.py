"""
Storage constants for DatavionOS.

Defines framework-wide constants used by the storage layer.

Storage is tenant-aware and provider-independent.
"""

from __future__ import annotations

###############################################################################
# Storage Providers
###############################################################################

LOCAL_STORAGE_PROVIDER = "local"

AWS_S3_STORAGE_PROVIDER = "s3"

AZURE_BLOB_STORAGE_PROVIDER = "azure"


DEFAULT_STORAGE_PROVIDER = LOCAL_STORAGE_PROVIDER


###############################################################################
# Path Handling
###############################################################################

STORAGE_PATH_SEPARATOR = "/"

TENANT_PATH_PREFIX = "tenants"

ORGANIZATION_PATH_PREFIX = "organizations"


###############################################################################
# File Limits
###############################################################################

DEFAULT_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

LARGE_FILE_SIZE_LIMIT = 500 * 1024 * 1024  # 500 MB


###############################################################################
# Supported Content Types
###############################################################################

PDF_CONTENT_TYPE = "application/pdf"

IMAGE_CONTENT_TYPES = (
    "image/jpeg",
    "image/png",
    "image/webp",
)

DOCUMENT_CONTENT_TYPES = (
    PDF_CONTENT_TYPE,
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


###############################################################################
# URL Expiration
###############################################################################

DEFAULT_SIGNED_URL_EXPIRATION = 3600  # seconds


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "AWS_S3_STORAGE_PROVIDER",
    "AZURE_BLOB_STORAGE_PROVIDER",
    "DEFAULT_MAX_FILE_SIZE",
    "DEFAULT_SIGNED_URL_EXPIRATION",
    "DEFAULT_STORAGE_PROVIDER",
    "DOCUMENT_CONTENT_TYPES",
    "IMAGE_CONTENT_TYPES",
    "LARGE_FILE_SIZE_LIMIT",
    "LOCAL_STORAGE_PROVIDER",
    "ORGANIZATION_PATH_PREFIX",
    "PDF_CONTENT_TYPE",
    "STORAGE_PATH_SEPARATOR",
    "TENANT_PATH_PREFIX",
)
