"""
Organization domain services.

This module contains the business orchestration for the
Organization aggregate root.

Responsibilities
----------------
* Organization lifecycle
* Business validation
* Transaction management
* Domain orchestration
* Audit extension points
* Domain event extension points
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.organizations.constants import (
    OrganizationStatus,
    VerificationStatus,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.validators.organization import (
    validate_unique_organization_code,
    validate_unique_organization_slug,
)

type OrganizationData = Mapping[str, Any]


# ============================================================
# Mutable fields
# ============================================================

MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "display_name",
        "slug",
        "category",
        "organization_type",
        "size",
        "email",
        "support_email",
        "phone",
        "website",
        "address",
        "city",
        "state",
        "country",
        "postal_code",
        "timezone",
        "registration_number",
        "tax_number",
        "license_number",
        "accreditation",
        "description",
        "is_demo",
    },
)


# ============================================================
# Internal helpers
# ============================================================


def _normalize_create_data(
    data: OrganizationData,
) -> dict[str, Any]:
    """
    Normalize organization data before persistence.
    """

    payload = dict(data)

    if "code" in payload and payload["code"]:
        payload["code"] = str(payload["code"]).strip().upper()

    if "slug" in payload and payload["slug"]:
        payload["slug"] = str(payload["slug"]).strip().lower()

    return payload


def _validate_unique_fields(
    payload: OrganizationData,
    *,
    tenant: Any,
    exclude_id: Any | None = None,
) -> None:
    """
    Validate tenant scoped uniqueness.
    """

    code = payload.get("code")

    if code:
        validate_unique_organization_code(
            tenant=tenant,
            code=str(code),
            exclude_id=exclude_id,
        )

    slug = payload.get("slug")

    if slug:
        validate_unique_organization_slug(
            tenant=tenant,
            slug=str(slug),
            exclude_id=exclude_id,
        )


def _audit(
    event: str,
    organization: Organization,
) -> None:
    """
    Audit extension point.

    Future integration:

    • Audit service
    • Activity log
    • SIEM
    """

    _ = (
        event,
        organization,
    )


def _publish_event(
    event: str,
    organization: Organization,
) -> None:
    """
    Domain event extension point.

    Future integration:

    • Workflow
    • Notifications
    • Webhooks
    • Search indexing
    • Analytics
    """

    _ = (
        event,
        organization,
    )


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_organization(
    *,
    validated_data: OrganizationData,
) -> Organization:
    """
    Create a new organization.
    """

    payload = _normalize_create_data(
        validated_data,
    )

    _validate_unique_fields(
        payload,
        tenant=payload["tenant"],
    )

    organization = Organization.objects.create(
        **payload,
    )

    _audit(
        "organization.created",
        organization,
    )

    _publish_event(
        "organization.created",
        organization,
    )

    return organization


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_organization(
    *,
    instance: Organization,
    validated_data: OrganizationData,
) -> Organization:
    """
    Update an organization.
    """

    if not validated_data:
        return instance

    payload = _normalize_create_data(
        validated_data,
    )

    _validate_unique_fields(
        payload,
        tenant=instance.tenant,
        exclude_id=instance.pk,
    )

    update_fields: list[str] = []

    for field, value in payload.items():
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
            "organization.updated",
            instance,
        )

        _publish_event(
            "organization.updated",
            instance,
        )

    return instance


# ============================================================
# Lifecycle validation
# ============================================================


def _ensure_not_archived(
    organization: Organization,
) -> None:
    """
    Prevent operations on archived organizations.
    """

    if organization.status == OrganizationStatus.ARCHIVED:
        raise ValueError(
            "Archived organizations cannot be modified.",
        )


def _ensure_not_verified(
    organization: Organization,
) -> None:
    """
    Prevent duplicate verification.
    """

    if organization.verification_status == VerificationStatus.VERIFIED:
        raise ValueError(
            "Organization is already verified.",
        )


# ============================================================
# Activate
# ============================================================


@transaction.atomic
def activate_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Activate an organization.
    """

    _ensure_not_archived(
        instance,
    )

    if instance.status == OrganizationStatus.ACTIVE:
        return instance

    instance.status = OrganizationStatus.ACTIVE

    instance.save(
        update_fields=[
            "status",
        ],
    )

    _audit(
        "organization.activated",
        instance,
    )

    _publish_event(
        "organization.activated",
        instance,
    )

    return instance


# ============================================================
# Deactivate
# ============================================================


@transaction.atomic
def deactivate_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Deactivate an organization.
    """

    _ensure_not_archived(
        instance,
    )

    if instance.status == OrganizationStatus.INACTIVE:
        return instance

    instance.status = OrganizationStatus.INACTIVE

    instance.save(
        update_fields=[
            "status",
        ],
    )

    _audit(
        "organization.deactivated",
        instance,
    )

    _publish_event(
        "organization.deactivated",
        instance,
    )

    return instance


# ============================================================
# Suspend
# ============================================================


@transaction.atomic
def suspend_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Suspend an organization.
    """

    _ensure_not_archived(
        instance,
    )

    if instance.status == OrganizationStatus.SUSPENDED:
        return instance

    instance.status = OrganizationStatus.SUSPENDED

    instance.save(
        update_fields=[
            "status",
        ],
    )

    _audit(
        "organization.suspended",
        instance,
    )

    _publish_event(
        "organization.suspended",
        instance,
    )

    return instance


# ============================================================
# Restore
# ============================================================


@transaction.atomic
def restore_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Restore an archived organization.
    """

    if instance.status != OrganizationStatus.ARCHIVED:
        return instance

    instance.status = OrganizationStatus.ACTIVE

    instance.save(
        update_fields=[
            "status",
        ],
    )

    _audit(
        "organization.restored",
        instance,
    )

    _publish_event(
        "organization.restored",
        instance,
    )

    return instance


# ============================================================
# Verification
# ============================================================


@transaction.atomic
def verify_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Mark an organization as verified.
    """

    _ensure_not_archived(
        instance,
    )

    _ensure_not_verified(
        instance,
    )

    instance.verification_status = VerificationStatus.VERIFIED

    instance.save(
        update_fields=[
            "verification_status",
        ],
    )

    _audit(
        "organization.verified",
        instance,
    )

    _publish_event(
        "organization.verified",
        instance,
    )

    return instance


# ============================================================
# Archive
# ============================================================


@transaction.atomic
def archive_organization(
    *,
    instance: Organization,
) -> Organization:
    """
    Archive an organization.

    Archive is a terminal lifecycle state.
    """

    if instance.status == OrganizationStatus.ARCHIVED:
        return instance

    instance.status = OrganizationStatus.ARCHIVED

    instance.save(
        update_fields=[
            "status",
        ],
    )

    _audit(
        "organization.archived",
        instance,
    )

    _publish_event(
        "organization.archived",
        instance,
    )

    return instance


# ============================================================
# Delete
# ============================================================


@transaction.atomic
def delete_organization(
    *,
    instance: Organization,
) -> None:
    """
    Soft-delete compatibility wrapper.

    Organizations are archived instead
    of being physically deleted.
    """

    archive_organization(
        instance=instance,
    )


# ============================================================
# Public exports
# ============================================================

__all__: tuple[str, ...] = (
    "OrganizationData",
    "activate_organization",
    "archive_organization",
    "create_organization",
    "deactivate_organization",
    "suspend_organization",
    "delete_organization",
    "restore_organization",
    "update_organization",
    "verify_organization",
)
