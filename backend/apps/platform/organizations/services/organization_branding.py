"""
Organization branding domain services.

Business services for organization branding.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.validators import (
    validate_hex_color,
)

type OrganizationBrandingData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "logo_path",
        "favicon_path",
        "primary_color",
        "secondary_color",
        "accent_color",
        "font_family",
        "theme_mode",
        "login_message",
    },
)


# ============================================================
# Internal extension hooks
# ============================================================


def _audit(
    event: str,
    branding: OrganizationBranding,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        branding,
    )


def _publish_event(
    event: str,
    branding: OrganizationBranding,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        branding,
    )


# ============================================================
# Validators
# ============================================================


def _validate_colors(
    data: Mapping[str, Any],
) -> None:
    """
    Validate branding colors.
    """

    for field in (
        "primary_color",
        "secondary_color",
        "accent_color",
    ):
        value = data.get(field)

        if value:
            validate_hex_color(value)


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_branding(
    *,
    validated_data: OrganizationBrandingData,
) -> OrganizationBranding:
    """
    Create organization branding.
    """

    _validate_colors(
        validated_data,
    )

    branding = OrganizationBranding.objects.create(
        **validated_data,
    )

    _audit(
        "organization.branding.created",
        branding,
    )

    _publish_event(
        "organization.branding.created",
        branding,
    )

    return branding


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_branding(
    *,
    instance: OrganizationBranding,
    validated_data: OrganizationBrandingData,
) -> OrganizationBranding:
    """
    Update organization branding.
    """

    if not validated_data:
        return instance

    _validate_colors(
        validated_data,
    )

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
            "organization.branding.updated",
            instance,
        )

        _publish_event(
            "organization.branding.updated",
            instance,
        )

    return instance


# ============================================================
# Delete
# ============================================================


@transaction.atomic
def delete_branding(
    *,
    instance: OrganizationBranding,
) -> None:
    """
    Delete branding configuration.
    """

    _audit(
        "organization.branding.deleted",
        instance,
    )

    _publish_event(
        "organization.branding.deleted",
        instance,
    )

    instance.delete()


# ============================================================
# Backwards-compatible aliases
# ============================================================

create_organization_branding = create_branding
update_organization_branding = update_branding
delete_organization_branding = delete_branding


__all__: tuple[str, ...] = (
    "OrganizationBrandingData",
    "create_branding",
    "create_organization_branding",
    "delete_branding",
    "delete_organization_branding",
    "update_branding",
    "update_organization_branding",
)
