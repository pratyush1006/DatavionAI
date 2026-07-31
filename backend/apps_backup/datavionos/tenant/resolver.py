"""
Tenant context resolver contracts.
"""

from __future__ import annotations

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.tenant.context import (
    TenantContext,
)


@runtime_checkable
class TenantResolver(
    Protocol,
):
    """
    Resolves the current tenant execution
    context from an execution source.
    """

    async def resolve(
        self,
        source: Any,
    ) -> TenantContext:
        """
        Resolve the tenant context.

        The execution source may represent:

        - HTTP requests
        - Background jobs
        - CLI commands
        - Message queue events
        - Webhooks
        - Scheduled tasks
        """


__all__ = [
    "TenantResolver",
]
