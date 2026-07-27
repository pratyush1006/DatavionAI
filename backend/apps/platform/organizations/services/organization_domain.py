"""
Organization domain domain services.

Business services for organization domain lifecycle.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.organizations.models import (
    OrganizationDomain,
)
from apps.platform.organizations.validators import (
    validate_domain_format,
    validate_primary_domain,
    validate_unique_domain,
)

type OrganizationDomainData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "domain",
        "domain_type",
        "is_primary",
        "verification_status",
        "verification_token_hash",
        "verified_at",
        "ssl_enabled",
        "ssl_expiry_date",
    },
)


# ============================================================
# Internal hooks
# ============================================================


def _audit(
    event: str,
    domain: OrganizationDomain,
) -> None:
    """
    Audit extension point.
    """

    _ = (
        event,
        domain,
    )


def _publish_event(
    event: str,
    domain: OrganizationDomain,
) -> None:
    """
    Domain event extension point.
    """

    _ = (
        event,
        domain,
    )


# ============================================================
# Validation
# ============================================================


def _normalize_domain(
    value: str,
) -> str:
    """
    Normalize domain names.
    """

    return value.strip().lower()


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_domain(
    *,
    validated_data: OrganizationDomainData,
) -> OrganizationDomain:
    """
    Create an organization domain.
    """

    validated_data = dict(validated_data)

    validated_data["domain"] = _normalize_domain(
        validated_data["domain"],
    )

    validate_domain_format(
        validated_data["domain"],
    )

    validate_unique_domain(
        validated_data["domain"],
    )

    domain = OrganizationDomain.objects.create(
        **validated_data,
    )

    _audit(
        "organization.domain.created",
        domain,
    )

    _publish_event(
        "organization.domain.created",
        domain,
    )

    return domain


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_domain(
    *,
    instance: OrganizationDomain,
    validated_data: OrganizationDomainData,
) -> OrganizationDomain:
    """
    Update an organization domain.
    """

    if not validated_data:
        return instance

    validated_data = dict(validated_data)

    if "domain" in validated_data:
        validated_data["domain"] = _normalize_domain(
            validated_data["domain"],
        )

        validate_domain_format(
            validated_data["domain"],
        )

        validate_unique_domain(
            validated_data["domain"],
            exclude_id=instance.pk,
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

        update_fields.append(
            field,
        )

    if update_fields:
        instance.save(
            update_fields=update_fields,
        )

        _audit(
            "organization.domain.updated",
            instance,
        )

        _publish_event(
            "organization.domain.updated",
            instance,
        )

    return instance


# ============================================================
# Primary domain
# ============================================================


@transaction.atomic
def set_primary_domain(
    *,
    instance: OrganizationDomain,
) -> OrganizationDomain:
    """
    Promote a domain to the primary organization domain.
    """

    if instance.is_primary:
        return instance

    validate_primary_domain(
        organization=instance.organization,
        exclude_id=instance.pk,
    )

    OrganizationDomain.objects.filter(
        organization=instance.organization,
        is_primary=True,
    ).exclude(
        pk=instance.pk,
    ).update(
        is_primary=False,
    )

    instance.is_primary = True

    instance.save(
        update_fields=[
            "is_primary",
        ],
    )

    _audit(
        "organization.domain.primary_changed",
        instance,
    )

    _publish_event(
        "organization.domain.primary_changed",
        instance,
    )

    return instance


# ============================================================
# Verification
# ============================================================


@transaction.atomic
def verify_domain(
    *,
    instance: OrganizationDomain,
) -> OrganizationDomain:
    """
    Mark a domain as verified.
    """

    if instance.verification_status == OrganizationDomain.VerificationStatus.VERIFIED:
        return instance

    instance.verification_status = OrganizationDomain.VerificationStatus.VERIFIED

    instance.verified_at = timezone.now()

    instance.save(
        update_fields=[
            "verification_status",
            "verified_at",
        ],
    )

    _audit(
        "organization.domain.verified",
        instance,
    )

    _publish_event(
        "organization.domain.verified",
        instance,
    )

    return instance


__all__: tuple[str, ...] = (
    "OrganizationDomainData",
    "create_domain",
    "set_primary_domain",
    "update_domain",
    "verify_domain",
)
