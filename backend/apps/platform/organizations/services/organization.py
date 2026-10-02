"""
Organization domain services.

This module contains the business orchestration for the
Organization aggregate root.

Responsibilities
----------------
* Organization lifecycle
* Business validation
* Geography hierarchy validation
* Transaction management
* Domain orchestration
* Audit extension points
* Domain event extension points
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)
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
        "country_ref",
        "region_ref",
        "city_ref",
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
        payload["code"] = (
            str(
                payload["code"],
            )
            .strip()
            .upper()
        )

    if "slug" in payload and payload["slug"]:
        payload["slug"] = (
            str(
                payload["slug"],
            )
            .strip()
            .lower()
        )

    return payload


def _validate_unique_fields(
    payload: OrganizationData,
    *,
    tenant: Any,
    exclude_id: Any | None = None,
) -> None:
    """
    Validate tenant-scoped uniqueness.
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


def _is_active_geography_record(
    instance: Any,
) -> bool:
    """
    Return whether a Geography record is active and not archived.
    """

    return bool(
        getattr(
            instance,
            "is_active",
            False,
        )
        and not getattr(
            instance,
            "is_deleted",
            False,
        )
    )


def _validate_geography_references(
    payload: OrganizationData,
    *,
    instance: Organization | None = None,
) -> None:
    """
    Validate the Organization Geography reference hierarchy.

    The Organization address hierarchy is:

        Country
           |
           +-- Region
                  |
                  +-- City

    For updates, the effective Geography state is calculated from the
    persisted Organization plus the supplied payload. This is essential
    for PATCH operations because omitted fields must retain their
    existing values.

    Rules
    -----
    * Geography references must be active and not archived.
    * A region requires a country.
    * A city requires a country.
    * A city requires a region.
    * The selected region must belong to the selected country.
    * The selected city must belong to the selected country.
    * The selected city must belong to the selected region.
    """

    if instance is None:
        country_ref = payload.get(
            "country_ref",
        )
        region_ref = payload.get(
            "region_ref",
        )
        city_ref = payload.get(
            "city_ref",
        )
    else:
        country_ref = (
            payload["country_ref"] if "country_ref" in payload else instance.country_ref
        )

        region_ref = (
            payload["region_ref"] if "region_ref" in payload else instance.region_ref
        )

        city_ref = payload["city_ref"] if "city_ref" in payload else instance.city_ref

    #
    # Nothing selected.
    #
    if country_ref is None and region_ref is None and city_ref is None:
        return

    #
    # Type validation.
    #
    if country_ref is not None and not isinstance(
        country_ref,
        Country,
    ):
        raise ValueError(
            "Invalid country Geography reference.",
        )

    if region_ref is not None and not isinstance(
        region_ref,
        AdministrativeRegion,
    ):
        raise ValueError(
            "Invalid region Geography reference.",
        )

    if city_ref is not None and not isinstance(
        city_ref,
        City,
    ):
        raise ValueError(
            "Invalid city Geography reference.",
        )

    #
    # Active/archive validation.
    #
    if country_ref is not None and not _is_active_geography_record(
        country_ref,
    ):
        raise ValueError(
            "The selected country is inactive or archived.",
        )

    if region_ref is not None and not _is_active_geography_record(
        region_ref,
    ):
        raise ValueError(
            "The selected region is inactive or archived.",
        )

    if city_ref is not None and not _is_active_geography_record(
        city_ref,
    ):
        raise ValueError(
            "The selected city is inactive or archived.",
        )

    #
    # Region requires country.
    #
    if region_ref is not None and country_ref is None:
        raise ValueError(
            "A country reference is required when a region reference is supplied.",
        )

    #
    # City requires country.
    #
    if city_ref is not None and country_ref is None:
        raise ValueError(
            "A country reference is required when a city reference is supplied.",
        )

    #
    # Enforce the complete Country → Region → City hierarchy.
    #
    if city_ref is not None and region_ref is None:
        raise ValueError(
            "A region reference is required when a city reference is supplied.",
        )

    #
    # Region must belong to the selected country.
    #
    if (
        region_ref is not None
        and country_ref is not None
        and region_ref.country_id != country_ref.pk
    ):
        raise ValueError(
            "The selected region does not belong to the selected country.",
        )

    #
    # City must belong to the selected country.
    #
    if (
        city_ref is not None
        and country_ref is not None
        and city_ref.country_id != country_ref.pk
    ):
        raise ValueError(
            "The selected city does not belong to the selected country.",
        )

    #
    # City must belong to the selected region.
    #
    if (
        city_ref is not None
        and region_ref is not None
        and city_ref.region_id != region_ref.pk
    ):
        raise ValueError(
            "The selected city does not belong to the selected region.",
        )


def _audit(
    event: str,
    organization: Organization,
) -> None:
    """
    Audit extension point.

    Future integration:

    * Audit service
    * Activity log
    * SIEM
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

    * Workflow
    * Notifications
    * Webhooks
    * Search indexing
    * Analytics
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
    tenant: Any | None = None,
    request_user: Any | None = None,
    **_: Any,
) -> Organization:
    """
    Create a new organization.
    """

    payload = _normalize_create_data(
        validated_data,
    )

    # The generic API mixin supplies the resolved tenant context.
    # Older callers may still provide it in validated_data; a
    # user's default organization is the final safe fallback
    # for authenticated requests.
    resolved_tenant = (
        tenant
        or payload.pop(
            "tenant",
            None,
        )
        or getattr(
            getattr(
                request_user,
                "organization",
                None,
            ),
            "tenant",
            None,
        )
    )

    if resolved_tenant is None:
        raise ValueError(
            "A tenant context is required to create an organization.",
        )

    payload["tenant"] = resolved_tenant

    _validate_unique_fields(
        payload,
        tenant=resolved_tenant,
    )

    _validate_geography_references(
        payload,
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
    tenant: Any | None = None,
    request_user: Any | None = None,
    organization: Any | None = None,
    **_: Any,
) -> Organization:
    """
    Update an organization.

    The API service layer supplies common request context.
    These context arguments are accepted here for compatibility
    with the shared service execution contract.

    The persisted organization tenant remains authoritative.

    Geography validation evaluates the complete effective state,
    combining persisted Geography references with supplied PATCH
    values.
    """

    if not validated_data:
        return instance

    payload = _normalize_create_data(
        validated_data,
    )

    instance_tenant = instance.tenant

    # Existing organizations must never be moved between
    # tenants as a side effect of an update request.
    if tenant is not None and tenant.pk != instance_tenant.pk:
        raise ValueError(
            "Organization tenant cannot be changed during update.",
        )

    # If the API request supplies an organization context,
    # ensure it refers to the same aggregate being updated.
    if organization is not None and organization.pk != instance.pk:
        raise ValueError(
            "Organization context does not match the organization being updated.",
        )

    # request_user is intentionally accepted as service context.
    # Authorization is handled by the API/RBAC layer.
    _ = request_user

    # Tenant-scoped uniqueness must always use the persisted
    # tenant of the organization being updated.
    _validate_unique_fields(
        payload,
        tenant=instance_tenant,
        exclude_id=instance.pk,
    )

    #
    # Validate Geography against the effective post-update state.
    #
    # This must happen before persistence so an invalid hierarchy
    # can never be written.
    #
    _validate_geography_references(
        payload,
        instance=instance,
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
