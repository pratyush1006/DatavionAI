"""
Read-only selectors for organization domains.

Selectors provide optimized read access for
organization domains and white-label routing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationDomain,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationDomainQuerySet = QuerySet[OrganizationDomain]


def get_domains(
    *,
    organization: Organization | Any | None = None,
    verification_status: str | None = None,
    domain_type: str | None = None,
) -> OrganizationDomainQuerySet:
    """
    Return organization domains.

    Supports filtering by organization,
    verification status and domain type.
    """

    queryset = OrganizationDomain.objects.select_related(
        "organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    if verification_status is not None:
        queryset = queryset.filter(
            verification_status=verification_status,
        )

    if domain_type is not None:
        queryset = queryset.filter(
            domain_type=domain_type,
        )

    return queryset


def get_domain_by_id(
    domain_id: Any,
) -> OrganizationDomain:
    """
    Return a domain by primary key.
    """

    return get_object_or_404(
        get_domains(),
        pk=domain_id,
    )


def get_primary_domain(
    organization: Organization | Any,
) -> OrganizationDomain:
    """
    Return the primary domain for an organization.
    """

    return get_object_or_404(
        get_domains(
            organization=organization,
        ),
        is_primary=True,
    )


def get_verified_domains(
    organization: Organization | Any | None = None,
) -> OrganizationDomainQuerySet:
    """
    Return verified domains.
    """

    return get_domains(
        organization=organization,
        verification_status=(OrganizationDomain.VerificationStatus.VERIFIED),
    )


def get_domain_by_name(
    domain: str,
) -> OrganizationDomain:
    """
    Return a domain by its hostname.
    """

    return get_object_or_404(
        OrganizationDomain.objects.select_related(
            "organization",
        ),
        domain=domain.strip().lower(),
    )


def domain_exists(
    domain: str,
) -> bool:
    """
    Check whether a domain exists.
    """

    return OrganizationDomain.objects.filter(
        domain=domain.strip().lower(),
    ).exists()


__all__: tuple[str, ...] = (
    "OrganizationDomainQuerySet",
    "domain_exists",
    "get_domain_by_id",
    "get_domain_by_name",
    "get_domains",
    "get_primary_domain",
    "get_verified_domains",
)
