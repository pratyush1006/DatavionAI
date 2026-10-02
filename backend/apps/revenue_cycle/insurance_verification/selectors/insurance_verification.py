"""Tenant-safe Insurance Verification query selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.insurance_verification.models import InsuranceVerification


def list_verifications(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    patient_id: UUID | None = None,
    request_reference: str | None = None,
) -> QuerySet[InsuranceVerification]:
    """List active records inside the exact tenant and organization scope."""

    queryset = (
        InsuranceVerification.objects.select_related(
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
    if request_reference:
        queryset = queryset.filter(request_reference=request_reference)
    return queryset


def get_verification(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Get one active verification inside the exact scope."""

    return InsuranceVerification.objects.select_related(
        "patient",
        "organization",
        "verified_by",
    ).get(
        pk=verification_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_verification_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Lock one active verification for mutation."""

    return (
        InsuranceVerification.objects.select_for_update()
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


def get_deleted_verification_for_update(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    verification_id: UUID,
) -> InsuranceVerification:
    """Lock one deleted verification for restoration."""

    return (
        InsuranceVerification.all_objects.select_for_update()
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
    "get_deleted_verification_for_update",
    "get_verification",
    "get_verification_for_update",
    "list_verifications",
)
