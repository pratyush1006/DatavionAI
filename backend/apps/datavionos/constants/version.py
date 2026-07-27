"""
Canonical version and identity metadata for DatavionOS.

This module defines the immutable identity of the DatavionOS kernel.
The values exposed here are considered stable public API and may be
referenced throughout the platform by backend services, CLI tools,
health endpoints, telemetry, and frontend applications.

Versioning follows Semantic Versioning (SemVer):

    MAJOR.MINOR.PATCH

Increment the version according to the following rules:

* MAJOR:
    Breaking API or compatibility changes.

* MINOR:
    Backward-compatible features.

* PATCH:
    Backward-compatible bug fixes.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------------
# Product Identity
# ---------------------------------------------------------------------------

DATAVIONOS_NAME: Final[str] = "DatavionOS"

DATAVIONOS_CODENAME: Final[str] = "Genesis"

DATAVIONOS_VENDOR: Final[str] = "DatavionAI"

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

MAJOR_VERSION: Final[int] = 1
MINOR_VERSION: Final[int] = 0
PATCH_VERSION: Final[int] = 0

DATAVIONOS_VERSION: Final[str] = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"

# Backward-compatible alias.
VERSION: Final[str] = DATAVIONOS_VERSION

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

SEMANTIC_VERSION: Final[tuple[int, int, int]] = (
    MAJOR_VERSION,
    MINOR_VERSION,
    PATCH_VERSION,
)

USER_AGENT: Final[str] = f"{DATAVIONOS_NAME}/{DATAVIONOS_VERSION}"

# ---------------------------------------------------------------------------
# Public Exports
# ---------------------------------------------------------------------------

__all__ = [
    "DATAVIONOS_NAME",
    "DATAVIONOS_CODENAME",
    "DATAVIONOS_VENDOR",
    "MAJOR_VERSION",
    "MINOR_VERSION",
    "PATCH_VERSION",
    "DATAVIONOS_VERSION",
    "VERSION",
    "SEMANTIC_VERSION",
    "USER_AGENT",
]
