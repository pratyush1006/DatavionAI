"""
Tenant services aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.tenant.resolver import (
    TenantResolver,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TenantServices:
    """
    Aggregates tenant runtime services.

    This object provides a stable entry
    point for tenant-specific platform
    capabilities.
    """

    resolver: TenantResolver


__all__ = [
    "TenantServices",
]
