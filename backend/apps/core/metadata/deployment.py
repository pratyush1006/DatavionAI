"""
Deployment metadata for the DatavionOS platform.

Provides deployment information used by:

- Health endpoints
- Observability
- Audit logs
- Incident debugging
- CI/CD traceability
"""

from __future__ import annotations

import os
import socket
from dataclasses import dataclass
from datetime import UTC, datetime

from apps.core.version import (
    BUILD_NUMBER,
    GIT_COMMIT,
    RELEASE_CHANNEL,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DeploymentMetadata:
    """
    Immutable deployment metadata.
    """

    build_number: str

    git_commit: str

    release_channel: str

    deployment_id: str

    environment: str

    region: str

    instance_id: str

    hostname: str

    deployed_at: str


DEPLOYMENT_METADATA = DeploymentMetadata(
    build_number=BUILD_NUMBER,
    git_commit=GIT_COMMIT,
    release_channel=RELEASE_CHANNEL,
    deployment_id=os.getenv(
        "DEPLOYMENT_ID",
        "local",
    ),
    environment=os.getenv(
        "ENVIRONMENT",
        "development",
    ),
    region=os.getenv(
        "DEPLOYMENT_REGION",
        "local",
    ),
    instance_id=os.getenv(
        "INSTANCE_ID",
        "local",
    ),
    hostname=socket.gethostname(),
    deployed_at=(
        datetime.now(UTC)
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    ),
)


__all__ = [
    "DEPLOYMENT_METADATA",
    "DeploymentMetadata",
]
