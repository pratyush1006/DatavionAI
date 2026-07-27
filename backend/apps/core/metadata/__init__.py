"""
Platform metadata package.
"""

from __future__ import annotations

from .application import (
    APPLICATION_METADATA,
    ApplicationMetadata,
)
from .deployment import (
    DEPLOYMENT_METADATA,
    DeploymentMetadata,
)
from .runtime import (
    RUNTIME_METADATA,
    RuntimeMetadata,
)

__all__ = [
    "APPLICATION_METADATA",
    "ApplicationMetadata",
    "DEPLOYMENT_METADATA",
    "DeploymentMetadata",
    "RUNTIME_METADATA",
    "RuntimeMetadata",
]
