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

from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)


class DatavionAnonRateThrottle(
    AnonRateThrottle,
):
    """
    Anonymous request throttle.
    """

    scope = "anonymous"


class DatavionUserRateThrottle(
    UserRateThrottle,
):
    """
    Authenticated user throttle.
    """

    scope = "user"


class DatavionScopedRateThrottle(
    ScopedRateThrottle,
):
    """
    Generic scoped throttle.
    """


class DatavionAIRateThrottle(
    ScopedRateThrottle,
):
    """
    AI endpoint throttle.

    Used for:

    - AI assistants
    - RAG queries
    - Agent execution
    """

    scope = "ai"


class DatavionExportRateThrottle(
    ScopedRateThrottle,
):
    """
    Export/report throttle.

    Used for:

    - CSV exports
    - Reports
    - Analytics extraction
    """

    scope = "export"


class DatavionTenantRateThrottle(
    ScopedRateThrottle,
):
    """
    Tenant-aware API throttle.

    Used for SaaS isolation.
    """

    scope = "tenant"


__all__: tuple[str, ...] = (
    "DatavionAnonRateThrottle",
    "DatavionUserRateThrottle",
    "DatavionScopedRateThrottle",
    "DatavionAIRateThrottle",
    "DatavionExportRateThrottle",
    "DatavionTenantRateThrottle",
)
