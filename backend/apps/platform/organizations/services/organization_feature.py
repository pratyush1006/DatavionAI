"""
Organization feature domain services.

Business services for organization feature entitlements.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.organizations.models import (
    OrganizationFeature,
)

type OrganizationFeatureData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "status",
        "settings",
        "enabled_at",
        "disabled_at",
    },
)


# ============================================================
# Internal hooks
# ============================================================


def _audit(
    event: str,
    feature: OrganizationFeature,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        feature,
    )


def _publish_event(
    event: str,
    feature: OrganizationFeature,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        feature,
    )


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_feature(
    *,
    validated_data: OrganizationFeatureData,
) -> OrganizationFeature:
    """
    Create an organization feature entitlement.
    """

    feature = OrganizationFeature.objects.create(
        **validated_data,
    )

    _audit(
        "organization.feature.created",
        feature,
    )

    _publish_event(
        "organization.feature.created",
        feature,
    )

    return feature


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_feature(
    *,
    instance: OrganizationFeature,
    validated_data: OrganizationFeatureData,
) -> OrganizationFeature:
    """
    Update an organization feature entitlement.
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

        update_fields.append(field)

    if update_fields:
        instance.save(
            update_fields=update_fields,
        )

        _audit(
            "organization.feature.updated",
            instance,
        )

        _publish_event(
            "organization.feature.updated",
            instance,
        )

    return instance


# ============================================================
# Enable
# ============================================================


@transaction.atomic
def enable_feature(
    *,
    instance: OrganizationFeature,
) -> OrganizationFeature:
    """
    Enable an organization feature.
    """

    if instance.status == OrganizationFeature.FeatureStatus.ENABLED:
        return instance

    instance.status = OrganizationFeature.FeatureStatus.ENABLED

    instance.enabled_at = timezone.now()
    instance.disabled_at = None

    instance.save(
        update_fields=[
            "status",
            "enabled_at",
            "disabled_at",
        ],
    )

    _audit(
        "organization.feature.enabled",
        instance,
    )

    _publish_event(
        "organization.feature.enabled",
        instance,
    )

    return instance


# ============================================================
# Disable
# ============================================================


@transaction.atomic
def disable_feature(
    *,
    instance: OrganizationFeature,
) -> OrganizationFeature:
    """
    Disable an organization feature.
    """

    if instance.status == OrganizationFeature.FeatureStatus.DISABLED:
        return instance

    instance.status = OrganizationFeature.FeatureStatus.DISABLED

    instance.disabled_at = timezone.now()

    instance.save(
        update_fields=[
            "status",
            "disabled_at",
        ],
    )

    _audit(
        "organization.feature.disabled",
        instance,
    )

    _publish_event(
        "organization.feature.disabled",
        instance,
    )

    return instance


__all__: tuple[str, ...] = (
    "OrganizationFeatureData",
    "create_feature",
    "disable_feature",
    "enable_feature",
    "update_feature",
)
