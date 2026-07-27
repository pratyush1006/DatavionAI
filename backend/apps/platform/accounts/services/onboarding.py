"""
DatavionOS tenant onboarding service.

Creates complete SaaS runtime boundary:

User
 |
Tenant
 |
Organization
 |
Membership
 |
RBAC Owner
"""

from __future__ import annotations

from django.db import transaction
from django.utils.text import slugify

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.tenancy.services import (
    TenantService,
)


class OnboardingService:
    """
    SaaS tenant provisioning service.
    """

    @staticmethod
    @transaction.atomic
    def provision(
        *,
        owner,
        organization_name: str,
        organization_type: str | None = None,
    ):
        """
        Provision complete tenant environment.
        """

        tenant = TenantService.create_tenant(
            name=organization_name,
            slug=slugify(
                organization_name,
            ),
            tenant_type=organization_type,
            owner=owner,
        )

        organization = Organization.objects.create(
            tenant=tenant,
            name=organization_name,
            display_name=organization_name,
            code=slugify(
                organization_name,
            )[:20].upper(),
            organization_type=organization_type,
        )

        return {
            "tenant": tenant,
            "organization": organization,
        }


__all__ = [
    "OnboardingService",
]
