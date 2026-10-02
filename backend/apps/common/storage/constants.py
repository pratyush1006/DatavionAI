"""
Storage constants for DatavionOS.

Defines infrastructure-level storage constants.
"""

from __future__ import annotations

DEFAULT_STORAGE_BACKEND = "local"


STORAGE_ALLOWED_CONTENT_TYPES = (
    "application/pdf",
    "image/jpeg",
    "image/png",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


MAX_FILE_SIZE_MB = 50


__all__: tuple[str, ...] = (
    "DEFAULT_STORAGE_BACKEND",
    "STORAGE_ALLOWED_CONTENT_TYPES",
    "MAX_FILE_SIZE_MB",
)
