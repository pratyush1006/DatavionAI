"""
Tenant services.

Business operations for tenant lifecycle management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction

from apps.platform.tenancy.constants import (
    TenantStatus,
    TenantType,
)
from apps.platform.tenancy.models import (
    Tenant,
)
from apps.platform.tenancy.services.membership import (
    TenantMembershipService,
)

if TYPE_CHECKING:
    from apps.platform.accounts.models import User


class TenantService:
    """
    Tenant lifecycle service.
    """

    @staticmethod
    @transaction.atomic
    def create_tenant(
        *,
        name: str,
        slug: str,
        tenant_type: str = TenantType.CLINIC,
        owner: User | None = None,
    ) -> Tenant:
        """
        Create a new tenant.

        If owner is provided,
        automatically creates owner membership.
        """

        tenant = Tenant.objects.create(
            name=name,
            slug=slug,
            tenant_type=tenant_type,
            status=TenantStatus.ACTIVE,
        )

        if owner:
            TenantMembershipService.create_membership(
                tenant=tenant,
                user=owner,
                is_owner=True,
            )

        return tenant

    @staticmethod
    @transaction.atomic
    def activate_tenant(
        tenant: Tenant,
    ) -> Tenant:
        """
        Activate tenant.
        """

        tenant.status = TenantStatus.ACTIVE

        tenant.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return tenant

    @staticmethod
    @transaction.atomic
    def suspend_tenant(
        tenant: Tenant,
    ) -> Tenant:
        """
        Suspend tenant.
        """

        tenant.status = TenantStatus.SUSPENDED

        tenant.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return tenant

    @staticmethod
    @transaction.atomic
    def update_settings(
        tenant: Tenant,
        settings: dict,
    ) -> Tenant:
        """
        Update tenant configuration.
        """

        tenant.settings = settings

        tenant.save(
            update_fields=[
                "settings",
                "updated_at",
            ],
        )

        return tenant


__all__ = ("TenantService",)
