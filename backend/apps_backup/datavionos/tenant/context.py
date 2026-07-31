"""
Tenant runtime context.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.tenant.organization import (
    Organization,
)
from apps.datavionos.tenant.subscription import (
    Subscription,
)
from apps.datavionos.tenant.tenant import (
    Tenant,
)
from apps.datavionos.tenant.user import (
    User,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TenantContext:
    """
    Immutable tenant execution context.

    This object represents the complete
    tenant-specific runtime state for the
    current execution.
    """

    tenant: Tenant

    organization: Organization | None

    subscription: Subscription | None

    user: User | None

    @property
    def tenant_id(
        self,
    ) -> str:
        """
        Return the current tenant identifier.
        """
        return self.tenant.id

    @property
    def organization_id(
        self,
    ) -> str | None:
        """
        Return the current organization identifier.
        """
        return self.organization.id if self.organization is not None else None

    @property
    def user_id(
        self,
    ) -> str | None:
        """
        Return the current user identifier.
        """
        return self.user.id if self.user is not None else None

    @property
    def timezone(
        self,
    ) -> str:
        """
        Return the effective timezone.

        Organization settings take precedence
        over tenant settings.
        """
        if self.organization is not None:
            return self.organization.timezone

        return self.tenant.timezone

    @property
    def locale(
        self,
    ) -> str:
        """
        Return the effective locale.

        Organization settings take precedence
        over tenant settings.
        """
        if self.organization is not None:
            return self.organization.locale

        return self.tenant.locale

    @property
    def currency(
        self,
    ) -> str:
        """
        Return the effective currency.

        Organization settings take precedence
        over tenant settings.
        """
        if self.organization is not None:
            return self.organization.currency

        return self.tenant.currency

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return whether a user is present.
        """
        return self.user is not None

    @property
    def is_subscription_active(
        self,
    ) -> bool:
        """
        Return whether the current subscription
        is active.
        """
        if self.subscription is None:
            return False

        return self.subscription.is_active


__all__ = [
    "TenantContext",
]
