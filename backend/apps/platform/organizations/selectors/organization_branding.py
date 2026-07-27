"""
Read-only selectors for organization branding.

Selectors provide optimized read access for
organization branding configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationBranding,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationBrandingQuerySet = QuerySet[OrganizationBranding]


def get_brandings(
    *,
    organization: Organization | Any | None = None,
) -> OrganizationBrandingQuerySet:
    """
    Return organization branding records.

    Supports optional organization filtering.
    """

    queryset = OrganizationBranding.objects.select_related(
        "organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    return queryset


def get_organization_brandings() -> OrganizationBrandingQuerySet:
    """
    Return all organization branding records.
    """

    return get_brandings()


def get_organization_branding_by_id(
    *,
    branding_id: Any,
) -> OrganizationBranding:
    """
    Return a branding record by primary key.
    """

    return get_object_or_404(
        get_brandings(),
        pk=branding_id,
    )


def get_organization_branding(
    organization: Organization | Any,
) -> OrganizationBranding:
    """
    Return branding for an organization.
    """

    return get_object_or_404(
        get_brandings(
            organization=organization,
        ),
    )


def get_organization_branding_by_organization(
    organization: Organization | Any,
) -> OrganizationBranding | None:
    """
    Return branding for an organization or ``None``.
    """

    return get_brandings(
        organization=organization,
    ).first()


def get_branding_by_domain(
    custom_domain: str,
) -> OrganizationBranding:
    """
    Return branding by custom domain.
    """

    return get_object_or_404(
        OrganizationBranding.objects.select_related(
            "organization",
        ),
        custom_domain=custom_domain.strip().lower(),
    )


def branding_exists(
    organization: Organization | Any,
) -> bool:
    """
    Check whether branding exists for an organization.
    """

    return OrganizationBranding.objects.filter(
        organization=organization,
    ).exists()


__all__: tuple[str, ...] = (
    "OrganizationBrandingQuerySet",
    "branding_exists",
    "get_branding_by_domain",
    "get_brandings",
    "get_organization_branding",
    "get_organization_branding_by_organization",
    "get_organization_branding_by_id",
    "get_organization_brandings",
)
