"""
Read-only selectors for organization features.

Selectors provide optimized read access for
organization feature entitlements.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationFeature,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationFeatureQuerySet = QuerySet[OrganizationFeature]


def get_features(
    *,
    organization: Organization | Any | None = None,
    status: str | None = None,
) -> OrganizationFeatureQuerySet:
    """
    Return organization feature entitlements.

    Supports filtering by organization
    and feature status.
    """

    queryset = OrganizationFeature.objects.select_related(
        "organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    if status is not None:
        queryset = queryset.filter(
            status=status,
        )

    return queryset


def get_feature_by_id(
    feature_id: Any,
) -> OrganizationFeature:
    """
    Return a feature entitlement by primary key.
    """

    return get_object_or_404(
        get_features(),
        pk=feature_id,
    )


def get_organization_features(
    organization: Organization | Any,
    *,
    status: str | None = None,
) -> OrganizationFeatureQuerySet:
    """
    Return feature entitlements for an organization.
    """

    return get_features(
        organization=organization,
        status=status,
    )


def get_enabled_features(
    organization: Organization | Any,
) -> OrganizationFeatureQuerySet:
    """
    Return enabled feature entitlements.
    """

    return get_features(
        organization=organization,
        status=OrganizationFeature.Status.ENABLED,
    )


def get_feature_by_code(
    *,
    organization: Organization | Any,
    feature_code: str,
) -> OrganizationFeature:
    """
    Return a feature entitlement by feature code.
    """

    return get_object_or_404(
        get_features(
            organization=organization,
        ),
        feature_code=feature_code.strip(),
    )


def feature_exists(
    *,
    organization: Organization | Any,
    feature_code: str,
) -> bool:
    """
    Check whether a feature entitlement exists.
    """

    return OrganizationFeature.objects.filter(
        organization=organization,
        feature_code=feature_code.strip(),
    ).exists()


__all__: tuple[str, ...] = (
    "OrganizationFeatureQuerySet",
    "feature_exists",
    "get_enabled_features",
    "get_feature_by_code",
    "get_feature_by_id",
    "get_features",
    "get_organization_features",
)
