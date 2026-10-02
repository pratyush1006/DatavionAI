"""
Platform version information for the Datavion AI platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

API_VERSION: Final[str] = "v1"

PLATFORM_NAME: Final[str] = "DatavionOS"

PLATFORM_CODE_NAME: Final[str] = "DatavionOS"


MAJOR_VERSION: Final[int] = 1
MINOR_VERSION: Final[int] = 0
PATCH_VERSION: Final[int] = 0


VERSION: Final[str] = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"


BUILD_NUMBER: Final[str] = "dev"

GIT_COMMIT: Final[str] = "unknown"

RELEASE_CHANNEL: Final[str] = "development"


@dataclass(
    frozen=True,
    slots=True,
)
class VersionInfo:
    """
    Immutable platform version information.
    """

    platform: str
    code_name: str
    version: str
    api_version: str
    build: str
    git_commit: str
    release_channel: str


VERSION_INFO = VersionInfo(
    platform=PLATFORM_NAME,
    code_name=PLATFORM_CODE_NAME,
    version=VERSION,
    api_version=API_VERSION,
    build=BUILD_NUMBER,
    git_commit=GIT_COMMIT,
    release_channel=RELEASE_CHANNEL,
)


__all__ = [
    "API_VERSION",
    "BUILD_NUMBER",
    "GIT_COMMIT",
    "MAJOR_VERSION",
    "MINOR_VERSION",
    "PATCH_VERSION",
    "PLATFORM_CODE_NAME",
    "PLATFORM_NAME",
    "RELEASE_CHANNEL",
    "VERSION",
    "VERSION_INFO",
    "VersionInfo",
]
