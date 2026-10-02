"""
Tenant resolution strategies.
"""

from __future__ import annotations

from apps.platform.organizations.models import (
    Organization,
)


class HeaderTenantResolver:
    """
    Resolve tenant context from request headers.

    Supported:

    HTTP_X_ORGANIZATION_ID
    """

    def resolve(
        self,
        request,
    ):

        organization_id = request.headers.get("X-Organization-ID")

        if not organization_id:
            return (
                None,
                None,
            )

        organization = (
            Organization.objects.select_related(
                "tenant",
            )
            .filter(
                id=organization_id,
            )
            .first()
        )

        if not organization:
            return (
                None,
                None,
            )

        return (
            organization.tenant,
            organization,
        )
