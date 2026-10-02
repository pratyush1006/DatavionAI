"""
DatavionAI API Lifecycle Constants.

Centralized API lifecycle definitions used throughout the DatavionAI
platform.

This module defines API lifecycle stages, compatibility modes,
deprecation metadata, sunset policies, version support, and feature
release channels.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# API Lifecycle
###############################################################################


class ApiLifecycle(StrEnum):
    """
    Supported API lifecycle stages.
    """

    EXPERIMENTAL = "experimental"

    ALPHA = "alpha"

    BETA = "beta"

    PREVIEW = "preview"

    GENERAL_AVAILABILITY = "ga"

    DEPRECATED = "deprecated"

    SUNSET = "sunset"

    RETIRED = "retired"


SUPPORTED_LIFECYCLE_STAGES: Final[tuple[str, ...]] = (
    ApiLifecycle.EXPERIMENTAL.value,
    ApiLifecycle.ALPHA.value,
    ApiLifecycle.BETA.value,
    ApiLifecycle.PREVIEW.value,
    ApiLifecycle.GENERAL_AVAILABILITY.value,
    ApiLifecycle.DEPRECATED.value,
    ApiLifecycle.SUNSET.value,
    ApiLifecycle.RETIRED.value,
)

###############################################################################
# Compatibility Modes
###############################################################################


class CompatibilityMode(StrEnum):
    """
    API compatibility guarantees.
    """

    STRICT = "strict"

    BACKWARD = "backward"

    FORWARD = "forward"

    BIDIRECTIONAL = "bidirectional"

    NONE = "none"


DEFAULT_COMPATIBILITY_MODE: Final[str] = CompatibilityMode.BACKWARD.value

###############################################################################
# Release Channels
###############################################################################

RELEASE_CHANNEL_EXPERIMENTAL: Final[str] = "experimental"

RELEASE_CHANNEL_ALPHA: Final[str] = "alpha"

RELEASE_CHANNEL_BETA: Final[str] = "beta"

RELEASE_CHANNEL_PREVIEW: Final[str] = "preview"

RELEASE_CHANNEL_STABLE: Final[str] = "stable"

SUPPORTED_RELEASE_CHANNELS: Final[tuple[str, ...]] = (
    RELEASE_CHANNEL_EXPERIMENTAL,
    RELEASE_CHANNEL_ALPHA,
    RELEASE_CHANNEL_BETA,
    RELEASE_CHANNEL_PREVIEW,
    RELEASE_CHANNEL_STABLE,
)

###############################################################################
# Deprecation Headers (RFC 9745 / Sunset RFC 8594)
###############################################################################

HEADER_DEPRECATION: Final[str] = "Deprecation"

HEADER_SUNSET: Final[str] = "Sunset"

HEADER_LINK: Final[str] = "Link"

HEADER_WARNING: Final[str] = "Warning"

###############################################################################
# Deprecation Metadata
###############################################################################

DEPRECATION_MESSAGE: Final[str] = "deprecated"

SUNSET_MESSAGE: Final[str] = "sunset"

MIGRATION_GUIDE: Final[str] = "migration_guide"

REPLACEMENT_API: Final[str] = "replacement_api"

REMOVAL_VERSION: Final[str] = "removal_version"

REMOVAL_DATE: Final[str] = "removal_date"

###############################################################################
# Version Support Policy
###############################################################################

SUPPORTED: Final[str] = "supported"

MAINTENANCE: Final[str] = "maintenance"

END_OF_LIFE: Final[str] = "end_of_life"

UNSUPPORTED: Final[str] = "unsupported"

###############################################################################
# Feature Availability
###############################################################################

FEATURE_ENABLED: Final[str] = "enabled"

FEATURE_DISABLED: Final[str] = "disabled"

FEATURE_PREVIEW: Final[str] = "preview"

FEATURE_EXPERIMENTAL: Final[str] = "experimental"

###############################################################################
# Reserved Lifecycle Values
###############################################################################

RESERVED_LIFECYCLE_VALUES: Final[frozenset[str]] = frozenset(
    {
        ApiLifecycle.EXPERIMENTAL.value,
        ApiLifecycle.ALPHA.value,
        ApiLifecycle.BETA.value,
        ApiLifecycle.PREVIEW.value,
        ApiLifecycle.GENERAL_AVAILABILITY.value,
        ApiLifecycle.DEPRECATED.value,
        ApiLifecycle.SUNSET.value,
        ApiLifecycle.RETIRED.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "ApiLifecycle",
    "CompatibilityMode",
)
