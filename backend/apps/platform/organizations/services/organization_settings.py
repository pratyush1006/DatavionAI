"""
Organization settings domain services.

Business services for OrganizationSettings.

Responsibilities
----------------
* Create settings
* Update settings
* Security configuration
* Notification preferences
* Localization configuration
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.organizations.models import (
    OrganizationSettings,
)

type OrganizationSettingsData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "language",
        "timezone",
        "currency",
        "date_format",
        "time_format",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "session_timeout_minutes",
        "mfa_required",
        "default_dashboard",
    },
)


# ============================================================
# Internal extension hooks
# ============================================================


def _audit(
    event: str,
    settings: OrganizationSettings,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        settings,
    )


def _publish_event(
    event: str,
    settings: OrganizationSettings,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        settings,
    )


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_settings(
    *,
    validated_data: OrganizationSettingsData,
) -> OrganizationSettings:
    """
    Create organization settings.
    """

    settings = OrganizationSettings.objects.create(
        **validated_data,
    )

    _audit(
        "organization.settings.created",
        settings,
    )

    _publish_event(
        "organization.settings.created",
        settings,
    )

    return settings


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_settings(
    *,
    instance: OrganizationSettings,
    validated_data: OrganizationSettingsData,
) -> OrganizationSettings:
    """
    Update organization settings.
    """

    if not validated_data:
        return instance

    update_fields: list[str] = []

    for field, value in validated_data.items():
        if field not in MUTABLE_FIELDS:
            continue

        setattr(
            instance,
            field,
            value,
        )

        update_fields.append(
            field,
        )

    if update_fields:
        instance.save(
            update_fields=update_fields,
        )

        _audit(
            "organization.settings.updated",
            instance,
        )

        _publish_event(
            "organization.settings.updated",
            instance,
        )

    return instance


# ============================================================
# MFA
# ============================================================


@transaction.atomic
def enable_mfa(
    *,
    instance: OrganizationSettings,
) -> OrganizationSettings:
    """
    Enable mandatory MFA.
    """

    if instance.mfa_required:
        return instance

    instance.mfa_required = True

    instance.save(
        update_fields=[
            "mfa_required",
        ],
    )

    _audit(
        "organization.settings.mfa.enabled",
        instance,
    )

    _publish_event(
        "organization.settings.mfa.enabled",
        instance,
    )

    return instance


@transaction.atomic
def disable_mfa(
    *,
    instance: OrganizationSettings,
) -> OrganizationSettings:
    """
    Disable mandatory MFA.
    """

    if not instance.mfa_required:
        return instance

    instance.mfa_required = False

    instance.save(
        update_fields=[
            "mfa_required",
        ],
    )

    _audit(
        "organization.settings.mfa.disabled",
        instance,
    )

    _publish_event(
        "organization.settings.mfa.disabled",
        instance,
    )

    return instance


__all__: tuple[str, ...] = (
    "OrganizationSettingsData",
    "create_settings",
    "disable_mfa",
    "enable_mfa",
    "update_settings",
)
