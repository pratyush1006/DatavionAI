"""
Organization domain validators.

Business validation helpers for tenant domains
and white-label routing.
"""

from __future__ import annotations

import re
from typing import Any

from django.apps import apps
from django.core.exceptions import ValidationError

DOMAIN_PATTERN = re.compile(
    r"^(?!-)(?:[a-z0-9-]{1,63}\.)+[a-z]{2,63}$",
    re.IGNORECASE,
)


def validate_domain_format(
    domain: str,
) -> None:
    """
    Validate domain format.
    """

    domain = domain.strip().lower()

    if not DOMAIN_PATTERN.fullmatch(domain):
        raise ValidationError(
            "Invalid domain format.",
        )


def validate_unique_domain(
    domain: str,
    *,
    exclude_id: Any = None,
) -> None:
    """
    Validate global domain uniqueness.
    """

    OrganizationDomain = apps.get_model(
        "organizations",
        "OrganizationDomain",
    )

    domain = domain.strip().lower()

    queryset = OrganizationDomain.objects.filter(
        domain=domain,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "Domain already exists.",
        )


def validate_primary_domain(
    *,
    organization: Any,
    exclude_id: Any = None,
) -> None:
    """
    Ensure an organization has only one primary domain.
    """

    OrganizationDomain = apps.get_model(
        "organizations",
        "OrganizationDomain",
    )

    queryset = OrganizationDomain.objects.filter(
        organization=organization,
        is_primary=True,
    )

    if exclude_id is not None:
        queryset = queryset.exclude(
            id=exclude_id,
        )

    if queryset.exists():
        raise ValidationError(
            "Organization already has a primary domain.",
        )


__all__: tuple[str, ...] = (
    "validate_domain_format",
    "validate_primary_domain",
    "validate_unique_domain",
)
