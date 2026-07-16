"""
Provider selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.clinical.providers.models import Provider
from apps.platform.organizations.models import Organization


def get_providers() -> QuerySet[Provider]:
    """
    Return all providers.
    """

    return Provider.objects.all()


def get_provider_by_id(
    *,
    provider_id,
) -> Provider:
    """
    Return a provider by ID.
    """

    return Provider.objects.get(
        id=provider_id,
    )


def get_organization_providers(
    *,
    organization: Organization,
) -> QuerySet[Provider]:
    """
    Return providers belonging to an organization.
    """

    return Provider.objects.filter(
        organization=organization,
    )


__all__ = [
    "get_organization_providers",
    "get_provider_by_id",
    "get_providers",
]
