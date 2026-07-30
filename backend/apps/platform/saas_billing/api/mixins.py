"""
DatavionOS SaaS Billing API mixins.

Shared API context utilities.

Responsibilities:

- Resolve organization context
- Support middleware injected organization
- Support API clients
- Support automated tests
- Maintain SaaS tenant isolation
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    Organization,
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

        Returns:

        Organization | None
        """

        # ----------------------------------------------------------
        # Middleware context
        # ----------------------------------------------------------

        organization = getattr(
            request,
            "organization",
            None,
        )

        if organization:
            return organization

        # ----------------------------------------------------------
        # Header fallback
        # ----------------------------------------------------------

        organization_id = request.headers.get(
            "X-Organization-ID",
        )

        if organization_id:
            organization = Organization.objects.filter(
                id=organization_id,
            ).first()

            if organization:
                return organization

        # ----------------------------------------------------------
        # Authenticated user fallback
        # ----------------------------------------------------------

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


__all__ = [
    "OrganizationContextMixin",
]
