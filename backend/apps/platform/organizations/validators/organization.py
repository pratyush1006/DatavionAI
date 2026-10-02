"""
Organization validators.

Business validation helpers for organizations.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from apps.platform.organizations.models import Organization


CODE_PATTERN = re.compile(
    r"^[A-Z0-9]{1,20}$",
)


def validate_organization_code(
    value: str,
) -> None:
    """
    Validate organization code format.
    """

    value = value.strip().upper()

    if not CODE_PATTERN.fullmatch(value):
        raise ValidationError(
            "Organization code must contain 1–20 uppercase letters or digits.",
        )


def validate_unique_organization_code(
    tenant: Any,
    code: str,
    *,
    exclude_id: Any = None,
) -> None:
    """
    Validate tenant-scoped organization code uniqueness.
    """

    Organization = apps.get_model(
        "organizations",
        "Organization",
    )

    code = code.strip().upper()

    queryset = Organization.objects.filter(
        tenant=tenant,
        code=code,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "Organization code already exists.",
        )


def validate_unique_organization_slug(
    tenant: Any,
    slug: str,
    *,
    exclude_id: Any = None,
) -> None:
    """
    Validate tenant-scoped organization slug uniqueness.
    """

    Organization = apps.get_model(
        "organizations",
        "Organization",
    )

    slug = slug.strip().lower()

    queryset = Organization.objects.filter(
        tenant=tenant,
        slug=slug,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "Organization slug already exists.",
        )


def validate_organization_active(
    organization: Organization,
) -> None:
    """
    Ensure the organization is active.
    """

    if not organization.is_active:
        raise ValidationError(
            "Organization is inactive.",
        )


__all__: tuple[str, ...] = (
    "validate_organization_active",
    "validate_organization_code",
    "validate_unique_organization_code",
    "validate_unique_organization_slug",
)
