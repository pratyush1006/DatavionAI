"""
Tenant context management.

Provides request-level tenant isolation
for DatavionOS SaaS platform.

Stores:

- Current tenant
- Current authenticated user
- Current tenant membership
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass

from apps.platform.accounts.models import (
    User,
)
from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TenantContext:
    """
    Runtime tenant execution context.

    Represents:

    User
        |
        |
    TenantMembership
        |
        |
    Tenant
    """

    tenant: Tenant

    user: User

    membership: TenantMembership


_current_tenant_context: ContextVar[TenantContext | None] = ContextVar(
    "current_tenant_context",
    default=None,
)


def set_tenant_context(
    context: TenantContext | None,
) -> None:
    """
    Set current tenant execution context.
    """

    _current_tenant_context.set(
        context,
    )


def get_tenant_context() -> TenantContext | None:
    """
    Return current tenant execution context.
    """

    return _current_tenant_context.get()


def set_current_tenant(
    tenant: Tenant | None,
) -> None:
    """
    Backward-compatible tenant setter.

    Deprecated:

    Use set_tenant_context()
    instead.
    """

    if tenant is None:
        set_tenant_context(
            None,
        )

        return

    current = get_tenant_context()

    if current is None:
        return

    set_tenant_context(
        TenantContext(
            tenant=tenant,
            user=current.user,
            membership=current.membership,
        ),
    )


def get_current_tenant() -> Tenant | None:
    """
    Return current tenant.

    Backward-compatible helper.
    """

    context = get_tenant_context()

    if context is None:
        return None

    return context.tenant


def clear_current_tenant() -> None:
    """
    Clear tenant execution context.
    """

    _current_tenant_context.set(
        None,
    )


__all__ = (
    "TenantContext",
    "set_tenant_context",
    "get_tenant_context",
    "set_current_tenant",
    "get_current_tenant",
    "clear_current_tenant",
)
