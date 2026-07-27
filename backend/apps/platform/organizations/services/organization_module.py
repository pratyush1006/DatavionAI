"""
Organization module domain services.

Business services for organization module entitlements.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.organizations.models import (
    OrganizationModule,
)

type OrganizationModuleData = Mapping[str, Any]


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
    module: OrganizationModule,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        module,
    )


def _publish_event(
    event: str,
    module: OrganizationModule,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        module,
    )


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_module(
    *,
    validated_data: OrganizationModuleData,
) -> OrganizationModule:
    """
    Create an organization module entitlement.
    """

    module = OrganizationModule.objects.create(
        **validated_data,
    )

    _audit(
        "organization.module.created",
        module,
    )

    _publish_event(
        "organization.module.created",
        module,
    )

    return module


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_module(
    *,
    instance: OrganizationModule,
    validated_data: OrganizationModuleData,
) -> OrganizationModule:
    """
    Update an organization module entitlement.
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
            "organization.module.updated",
            instance,
        )

        _publish_event(
            "organization.module.updated",
            instance,
        )

    return instance


# ============================================================
# Enable
# ============================================================


@transaction.atomic
def enable_module(
    *,
    instance: OrganizationModule,
) -> OrganizationModule:
    """
    Enable an organization module.
    """

    if instance.status == OrganizationModule.Status.ENABLED:
        return instance

    instance.status = OrganizationModule.Status.ENABLED
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
        "organization.module.enabled",
        instance,
    )

    _publish_event(
        "organization.module.enabled",
        instance,
    )

    return instance


# ============================================================
# Disable
# ============================================================


@transaction.atomic
def disable_module(
    *,
    instance: OrganizationModule,
) -> OrganizationModule:
    """
    Disable an organization module.
    """

    if instance.status == OrganizationModule.Status.DISABLED:
        return instance

    instance.status = OrganizationModule.Status.DISABLED
    instance.disabled_at = timezone.now()

    instance.save(
        update_fields=[
            "status",
            "disabled_at",
        ],
    )

    _audit(
        "organization.module.disabled",
        instance,
    )

    _publish_event(
        "organization.module.disabled",
        instance,
    )

    return instance


__all__: tuple[str, ...] = (
    "OrganizationModuleData",
    "create_module",
    "disable_module",
    "enable_module",
    "update_module",
)
