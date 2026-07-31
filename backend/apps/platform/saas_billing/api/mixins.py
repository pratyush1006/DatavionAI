"""
DatavionOS SaaS Billing API mixins.

Shared API context utilities.

Responsibilities:

- Resolve organization context
- Resolve plan resources
- Support middleware injected organization
- Support API clients
- Support automated tests
- Maintain SaaS tenant isolation
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.saas_billing.models import (
    Plan,
)


class OrganizationContextMixin:
    """
    Organization context resolver for SaaS APIs.

    Resolution order:

    1. Middleware injected organization
    2. Request organization attribute
    3. X-Organization-ID header
    4. User primary organization role

    Designed for:

    - Multi-tenant SaaS
    - API clients
    - Automated tests
    - Background integrations
    """

    def get_organization(
        self,
        request,
    ):
        """
        Resolve current organization.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        if organization:
            return organization

        organization_id = request.headers.get(
            "X-Organization-ID",
        )

        if organization_id:
            organization = Organization.objects.filter(
                id=organization_id,
            ).first()

            if organization:
                return organization

        user = getattr(
            request,
            "user",
            None,
        )

        if user and user.is_authenticated:
            organization_role = (
                user.organization_roles.filter(
                    is_active=True,
                )
                .select_related(
                    "organization",
                )
                .first()
            )

            if organization_role:
                return organization_role.organization

        return None


class PlanLookupMixin:
    """
    SaaS Billing plan resolver.

    Shared by:

    - Update Plan API
    - Activate Plan API
    - Deactivate Plan API
    - Archive Plan API
    """

    def get_plan(
        self,
        pk,
    ) -> Plan:
        """
        Retrieve plan by UUID.

        Raises:

        Plan.DoesNotExist
        """

        return Plan.objects.get(
            id=pk,
        )


__all__ = [
    "OrganizationContextMixin",
    "PlanLookupMixin",
]
