"""
Application metadata for the DatavionOS platform.

Provides immutable platform identity information used by:

- Health endpoints
- API documentation
- Monitoring
- Telemetry
- Audit systems
- Support diagnostics
"""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings

from apps.core.enums import Environment
from apps.core.version import (
    API_VERSION,
    BUILD_NUMBER,
    PLATFORM_CODE_NAME,
    PLATFORM_NAME,
    RELEASE_CHANNEL,
    VERSION,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ApplicationMetadata:
    """
    Immutable application metadata.
    """

    name: str

    code_name: str

    version: str

    api_version: str

    environment: Environment

    build_number: str

    release_channel: str


APPLICATION_METADATA = ApplicationMetadata(
    name=PLATFORM_NAME,
    code_name=PLATFORM_CODE_NAME,
    version=VERSION,
    api_version=API_VERSION,
    environment=Environment(
        getattr(
            settings,
            "ENVIRONMENT",
            Environment.DEVELOPMENT,
        )
    ),
    build_number=BUILD_NUMBER,
    release_channel=RELEASE_CHANNEL,
)


__all__ = [
    "APPLICATION_METADATA",
    "ApplicationMetadata",
]
