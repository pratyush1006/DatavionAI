"""Tenant-safe Eligibility query selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.eligibility.models import Eligibility


def list_eligibility(
    *, tenant_id: UUID, organization_id: UUID, patient_id: UUID | None = None
) -> QuerySet[Eligibility]:
    """List active records within the exact tenant and organization scope."""
    qs = Eligibility.objects.select_related(
        "patient", "organization", "verified_by"
    ).filter(organization_id=organization_id, organization__tenant_id=tenant_id)
    if patient_id is not None:
        qs = qs.filter(patient_id=patient_id)
    return qs.order_by("-requested_at")


def get_eligibility(
    *, tenant_id: UUID, organization_id: UUID, eligibility_id: UUID
) -> Eligibility:
    """Get one active record within the exact tenant and organization scope."""
    return Eligibility.objects.select_related(
        "patient", "organization", "verified_by"
    ).get(
        pk=eligibility_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_eligibility_for_update(
    *, tenant_id: UUID, organization_id: UUID, eligibility_id: UUID
) -> Eligibility:
    """Lock one active record for a mutation."""
    return (
        Eligibility.objects.select_for_update()
        .select_related("patient", "organization")
        .get(
            pk=eligibility_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
    )


def get_deleted_eligibility_for_update(
    *, tenant_id: UUID, organization_id: UUID, eligibility_id: UUID
) -> Eligibility:
    """Lock one deleted record for restoration."""
    return (
        Eligibility.all_objects.select_for_update()
        .select_related("patient", "organization")
        .get(
            pk=eligibility_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            is_deleted=True,
        )
    )


__all__ = (
    "get_deleted_eligibility_for_update",
    "get_eligibility",
    "get_eligibility_for_update",
    "list_eligibility",
)
