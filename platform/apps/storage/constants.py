"""
Constants used by the Storage application.
"""

from __future__ import annotations

# ============================================================================
# Storage Providers
# ============================================================================

STORAGE_PROVIDER_LOCAL = "LOCAL"
STORAGE_PROVIDER_S3 = "S3"
STORAGE_PROVIDER_AZURE = "AZURE"
STORAGE_PROVIDER_GCS = "GCS"

STORAGE_PROVIDER_CHOICES = (
    (STORAGE_PROVIDER_LOCAL, "Local"),
    (STORAGE_PROVIDER_S3, "Amazon S3"),
    (STORAGE_PROVIDER_AZURE, "Azure Blob Storage"),
    (STORAGE_PROVIDER_GCS, "Google Cloud Storage"),
)

# ============================================================================
# Asset Visibility
# ============================================================================

ASSET_VISIBILITY_PRIVATE = "PRIVATE"
ASSET_VISIBILITY_PUBLIC = "PUBLIC"

ASSET_VISIBILITY_CHOICES = (
    (ASSET_VISIBILITY_PRIVATE, "Private"),
    (ASSET_VISIBILITY_PUBLIC, "Public"),
)

# ============================================================================
# Asset Status
# ============================================================================

ASSET_STATUS_UPLOADING = "UPLOADING"
ASSET_STATUS_READY = "READY"
ASSET_STATUS_FAILED = "FAILED"
ASSET_STATUS_DELETED = "DELETED"

ASSET_STATUS_CHOICES = (
    (ASSET_STATUS_UPLOADING, "Uploading"),
    (ASSET_STATUS_READY, "Ready"),
    (ASSET_STATUS_FAILED, "Failed"),
    (ASSET_STATUS_DELETED, "Deleted"),
)

# ============================================================================
# Asset Categories
# ============================================================================

ASSET_CATEGORY_IMAGE = "IMAGE"
ASSET_CATEGORY_DOCUMENT = "DOCUMENT"
ASSET_CATEGORY_VIDEO = "VIDEO"
ASSET_CATEGORY_AUDIO = "AUDIO"
ASSET_CATEGORY_ARCHIVE = "ARCHIVE"
ASSET_CATEGORY_OTHER = "OTHER"

ASSET_CATEGORY_CHOICES = (
    (ASSET_CATEGORY_IMAGE, "Image"),
    (ASSET_CATEGORY_DOCUMENT, "Document"),
    (ASSET_CATEGORY_VIDEO, "Video"),
    (ASSET_CATEGORY_AUDIO, "Audio"),
    (ASSET_CATEGORY_ARCHIVE, "Archive"),
    (ASSET_CATEGORY_OTHER, "Other"),
)

# ============================================================================
# Default Provider
# ============================================================================

DEFAULT_STORAGE_PROVIDER = STORAGE_PROVIDER_LOCAL
