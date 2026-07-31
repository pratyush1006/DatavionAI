"""
Reusable API throttling classes for the DatavionOS framework.

Provides platform-wide throttling policies:

- Anonymous users
- Authenticated users
- Tenant APIs
- AI workloads
- Export workloads
"""

from __future__ import annotations

from typing import Final

from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)


class DatavionAnonRateThrottle(AnonRateThrottle):
    """
    Anonymous request throttle.
    """

    scope: Final[str] = "anonymous"


class DatavionUserRateThrottle(UserRateThrottle):
    """
    Authenticated user throttle.
    """

    scope: Final[str] = "user"


class DatavionScopedRateThrottle(ScopedRateThrottle):
    """
    Generic scoped throttle.

    Individual views should define
    ``throttle_scope`` as needed.
    """


class DatavionAIRateThrottle(ScopedRateThrottle):
    """
    AI endpoint throttle.

    Used for:

    - AI assistants
    - RAG queries
    - Agent execution
    """

    scope: Final[str] = "ai"


class DatavionExportRateThrottle(ScopedRateThrottle):
    """
    Export/report throttle.

    Used for:

    - CSV exports
    - Reports
    - Analytics extraction
    """

    scope: Final[str] = "export"


class DatavionTenantRateThrottle(ScopedRateThrottle):
    """
    Tenant-aware API throttle.

    Used for SaaS isolation.

    Individual views should define
    ``throttle_scope`` when a more
    specific tenant policy is required.
    """

    scope: Final[str] = "tenant"


__all__: Final[tuple[str, ...]] = (
    "DatavionAnonRateThrottle",
    "DatavionUserRateThrottle",
    "DatavionScopedRateThrottle",
    "DatavionAIRateThrottle",
    "DatavionExportRateThrottle",
    "DatavionTenantRateThrottle",
)
