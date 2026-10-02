"""
DatavionAI API Metadata Constants.

This module contains immutable platform and API metadata shared across the
DatavionAI backend. These constants are intended for use by OpenAPI schema
generation, API documentation, versioning, diagnostics, health endpoints,
client SDKs, and platform services.

Guidelines
----------
- Keep all values immutable.
- Do not place business logic in this module.
- Runtime configuration belongs in the configuration subsystem.
- This module is safe to import anywhere.

Copyright (c) DatavionAI.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Platform Metadata
###############################################################################

PLATFORM_NAME: Final[str] = "DatavionAI"

PLATFORM_SHORT_NAME: Final[str] = "datavionai"

PLATFORM_TAGLINE: Final[str] = "The AI Operating System for Healthcare"

PLATFORM_DESCRIPTION: Final[str] = "Enterprise AI-Native Healthcare Platform."

PLATFORM_VENDOR: Final[str] = "DatavionAI"

PLATFORM_COPYRIGHT: Final[str] = "Copyright © DatavionAI. All rights reserved."

###############################################################################
# API Metadata
###############################################################################

API_NAME: Final[str] = "DatavionAI API"

API_TITLE: Final[str] = API_NAME

API_DESCRIPTION: Final[str] = "Enterprise REST API for the DatavionAI Platform."

API_LICENSE: Final[str] = "Proprietary"

API_CONTACT_NAME: Final[str] = "DatavionAI"

API_CONTACT_EMAIL: Final[str] = ""

API_CONTACT_URL: Final[str] = ""

API_TERMS_OF_SERVICE: Final[str] = ""

###############################################################################
# Version Enumeration
###############################################################################


class ApiVersion(StrEnum):
    """
    Supported API versions.
    """

    V1 = "v1"


###############################################################################
# Version Information
###############################################################################

API_VERSION: Final[str] = ApiVersion.V1.value

DEFAULT_API_VERSION: Final[str] = ApiVersion.V1.value

LATEST_API_VERSION: Final[str] = ApiVersion.V1.value

SUPPORTED_API_VERSIONS: Final[tuple[str, ...]] = (ApiVersion.V1.value,)

###############################################################################
# Release Information
###############################################################################

API_RELEASE_STAGE: Final[str] = "stable"

API_BUILD_NUMBER: Final[str] = ""

API_BUILD_DATE: Final[str] = ""

API_GIT_COMMIT: Final[str] = ""

###############################################################################
# Environment Names
###############################################################################

ENV_DEVELOPMENT: Final[str] = "development"

ENV_TESTING: Final[str] = "testing"

ENV_STAGING: Final[str] = "staging"

ENV_PRODUCTION: Final[str] = "production"

SUPPORTED_ENVIRONMENTS: Final[tuple[str, ...]] = (
    ENV_DEVELOPMENT,
    ENV_TESTING,
    ENV_STAGING,
    ENV_PRODUCTION,
)

###############################################################################
# Regional Defaults
###############################################################################

DEFAULT_LANGUAGE: Final[str] = "en"

DEFAULT_LOCALE: Final[str] = "en_US"

DEFAULT_TIMEZONE: Final[str] = "UTC"

DEFAULT_CHARACTER_SET: Final[str] = "utf-8"

###############################################################################
# Date / Time Formats
###############################################################################

DATE_FORMAT: Final[str] = "%Y-%m-%d"

TIME_FORMAT: Final[str] = "%H:%M:%S"

DATETIME_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S%z"

ISO8601_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S.%f%z"

###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "ApiVersion",
    "PLATFORM_NAME",
    "PLATFORM_SHORT_NAME",
    "PLATFORM_TAGLINE",
    "PLATFORM_DESCRIPTION",
    "PLATFORM_VENDOR",
    "PLATFORM_COPYRIGHT",
    "API_NAME",
    "API_TITLE",
    "API_DESCRIPTION",
    "API_LICENSE",
    "API_CONTACT_NAME",
    "API_CONTACT_EMAIL",
    "API_CONTACT_URL",
    "API_TERMS_OF_SERVICE",
    "API_VERSION",
    "DEFAULT_API_VERSION",
    "LATEST_API_VERSION",
    "SUPPORTED_API_VERSIONS",
    "API_RELEASE_STAGE",
    "API_BUILD_NUMBER",
    "API_BUILD_DATE",
    "API_GIT_COMMIT",
    "ENV_DEVELOPMENT",
    "ENV_TESTING",
    "ENV_STAGING",
    "ENV_PRODUCTION",
    "SUPPORTED_ENVIRONMENTS",
    "DEFAULT_LANGUAGE",
    "DEFAULT_LOCALE",
    "DEFAULT_TIMEZONE",
    "DEFAULT_CHARACTER_SET",
    "DATE_FORMAT",
    "TIME_FORMAT",
    "DATETIME_FORMAT",
    "ISO8601_FORMAT",
)
