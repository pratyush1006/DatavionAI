"""
Organization domain services.

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
    validate_unique_domain,
)

type OrganizationDomainData = Mapping[str, Any]


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


def _normalize_domain(
    value: str,
) -> str:
    """
    Normalize a domain hostname.
    """

    return value.strip().lower()


@transaction.atomic
def create_organization_domain(
    *,
    validated_data: OrganizationDomainData,
    request_user: Any = None,
    tenant: Any = None,
    organization: Any = None,
) -> OrganizationDomain:
    """
    Create an organization domain.
    """

    _ = (
        request_user,
        tenant,
    )

    data = dict(validated_data)

    if organization is not None:
        data.setdefault(
            "organization",
            organization,
        )

    domain_value = data.get("domain")

    if not isinstance(domain_value, str):
        raise ValueError(
            "Domain must be provided as a string.",
        )

    data["domain"] = _normalize_domain(
        domain_value,
    )

    validate_domain_format(
        data["domain"],
    )

    validate_unique_domain(
        data["domain"],
    )

    domain = OrganizationDomain.objects.create(
        **data,
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


@transaction.atomic
def update_organization_domain(
    *,
    instance: OrganizationDomain,
    validated_data: OrganizationDomainData,
    request_user: Any = None,
    tenant: Any = None,
    organization: Any = None,
) -> OrganizationDomain:
    """
    Update an organization domain.
    """

    _ = (
        request_user,
        tenant,
        organization,
    )

    if not validated_data:
        return instance

    data = dict(validated_data)

    if "domain" in data:
        domain_value = data["domain"]

        if not isinstance(domain_value, str):
            raise ValueError(
                "Domain must be provided as a string.",
            )

        data["domain"] = _normalize_domain(
            domain_value,
        )

        validate_domain_format(
            data["domain"],
        )

        validate_unique_domain(
            data["domain"],
            exclude_id=instance.pk,
        )

    update_fields: list[str] = []

    for field, value in data.items():
        if field not in MUTABLE_FIELDS:
            continue

        if getattr(instance, field) == value:
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


@transaction.atomic
def set_primary_domain(
    *,
    instance: OrganizationDomain,
    request_user: Any = None,
    tenant: Any = None,
    organization: Any = None,
) -> OrganizationDomain:
    """
    Set a domain as the organization's primary domain.

    Any existing primary domain is demoted before
    the requested domain is promoted.
    """

    _ = (
        request_user,
        tenant,
        organization,
    )

    if instance.is_deleted:
        raise ValueError(
            "A deleted domain cannot be made primary.",
        )

    if instance.is_primary:
        return instance

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


@transaction.atomic
def verify_organization_domain(
    *,
    instance: OrganizationDomain,
    request_user: Any = None,
    tenant: Any = None,
    organization: Any = None,
) -> OrganizationDomain:
    """
    Mark a domain as verified.
    """

    _ = (
        request_user,
        tenant,
        organization,
    )

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


@transaction.atomic
def delete_organization_domain(
    *,
    instance: OrganizationDomain,
    request_user: Any = None,
    tenant: Any = None,
    organization: Any = None,
) -> OrganizationDomain:
    """
    Soft-delete an organization domain.
    """

    _ = (
        tenant,
        organization,
    )

    if instance.is_deleted:
        return instance

    instance.soft_delete(
        user_id=getattr(
            request_user,
            "pk",
            None,
        ),
    )

    _audit(
        "organization.domain.deleted",
        instance,
    )

    _publish_event(
        "organization.domain.deleted",
        instance,
    )

    return instance


# ------------------------------------------------------------------
# Backward-compatible aliases
# ------------------------------------------------------------------

create_domain = create_organization_domain

update_domain = update_organization_domain

verify_domain = verify_organization_domain


__all__: tuple[str, ...] = (
    "OrganizationDomainData",
    "create_domain",
    "create_organization_domain",
    "delete_organization_domain",
    "set_primary_domain",
    "update_domain",
    "update_organization_domain",
    "verify_domain",
    "verify_organization_domain",
)
