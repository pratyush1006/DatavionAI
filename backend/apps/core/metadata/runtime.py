"""
Runtime metadata for the DatavionOS platform.

Provides runtime information used by:

- Health endpoints
- Monitoring systems
- Diagnostics
- Support tooling
- Deployment troubleshooting
"""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass

import django


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeMetadata:
    """
    Immutable runtime metadata.
    """

    python_version: str

    django_version: str

    implementation: str

    operating_system: str

    platform: str

    architecture: str

    processor: str

    containerized: bool


def _is_containerized() -> bool:
    """
    Detect whether application is running inside a container.
    """

    return os.path.exists(
        "/.dockerenv",
    ) or bool(
        os.getenv(
            "KUBERNETES_SERVICE_HOST",
        )
    )


RUNTIME_METADATA = RuntimeMetadata(
    python_version=sys.version.split()[0],
    django_version=django.get_version(),
    implementation=platform.python_implementation(),
    operating_system=platform.system(),
    platform=platform.platform(),
    architecture=platform.machine(),
    processor=platform.processor(),
    containerized=_is_containerized(),
)


__all__ = [
    "RUNTIME_METADATA",
    "RuntimeMetadata",
]
