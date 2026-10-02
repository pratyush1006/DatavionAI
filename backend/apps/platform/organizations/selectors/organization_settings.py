"""
Read-only selectors for organization settings.

Selectors provide optimized read access for
organization configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationSettings,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationSettingsQuerySet = QuerySet[OrganizationSettings]


def get_settings(
    *,
    organization: Organization | Any | None = None,
) -> OrganizationSettingsQuerySet:
    """
    Return organization settings.

    Supports optional organization filtering.
    """

    queryset = OrganizationSettings.objects.select_related(
        "organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    return queryset


def get_organization_settings(
    organization: Organization | Any,
) -> OrganizationSettings:
    """
    Return settings for an organization.
    """

    return get_object_or_404(
        get_settings(
            organization=organization,
        ),
    )


def get_mfa_required_settings() -> OrganizationSettingsQuerySet:
    """
    Return organizations requiring MFA.
    """

    return OrganizationSettings.objects.filter(
        mfa_required=True,
    ).select_related(
        "organization",
    )


def get_email_enabled_settings() -> OrganizationSettingsQuerySet:
    """
    Return organizations with email notifications enabled.
    """

    return OrganizationSettings.objects.filter(
        email_notifications=True,
    ).select_related(
        "organization",
    )


__all__: tuple[str, ...] = (
    "OrganizationSettingsQuerySet",
    "get_email_enabled_settings",
    "get_mfa_required_settings",
    "get_organization_settings",
    "get_settings",
)
