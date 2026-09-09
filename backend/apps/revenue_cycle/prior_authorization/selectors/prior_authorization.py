"""Tenant-safe Prior Authorization query selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


def list_verifications(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    patient_id: UUID | None = None,
) -> QuerySet[PriorAuthorization]:
    """List active records inside the exact tenant and organization scope."""

    queryset = (
        PriorAuthorization.objects.select_related(
            "patient",
            "organization",
            "verified_by",
        )
        .filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .order_by("-requested_at")
    )
    if patient_id is not None:
        queryset = queryset.filter(patient_id=patient_id)
    return queryset


def get_verification(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> PriorAuthorization:
    """Get one active verification inside the exact scope."""

    return PriorAuthorization.objects.select_related(
        "patient",
        "organization",
        "verified_by",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_authorization_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> PriorAuthorization:
    """Lock one active verification for mutation."""

    return (
        PriorAuthorization.objects.select_for_update()
        .select_related(
            "patient",
            "organization",
        )
        .get(
            pk=verification_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
    )


def get_deleted_authorization_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> PriorAuthorization:
    """Lock one deleted verification for restoration."""

    return (
        PriorAuthorization.all_objects.select_for_update()
        .select_related(
            "patient",
            "organization",
        )
        .get(
            pk=verification_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            is_deleted=True,
        )
    )


__all__ = (
    "get_deleted_authorization_for_update",
    "get_verification",
    "get_authorization_for_update",
    "list_verifications",
)
