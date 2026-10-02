"""
Selectors for tenant-safe Patient Referral reads.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.referrals.models import PatientReferral


def get_referral_queryset(
    *,
    tenant_id,
    organization_id,
    include_deleted: bool = False,
) -> QuerySet:
    """Return referrals restricted to one tenant and organization."""

    manager = (
        PatientReferral.all_objects if include_deleted else PatientReferral.objects
    )

    return manager.filter(
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    ).select_related(
        "organization",
        "patient",
    )


def list_referrals(
    *,
    tenant_id,
    organization_id,
    patient_id=None,
    status=None,
    include_deleted: bool = False,
) -> QuerySet:
    """List referrals using the canonical tenant boundary."""

    queryset = get_referral_queryset(
        tenant_id=tenant_id,
        organization_id=organization_id,
        include_deleted=include_deleted,
    )

    if patient_id is not None:
        queryset = queryset.filter(patient_id=patient_id)

    if status is not None:
        queryset = queryset.filter(status=status)

    return queryset


def get_referral(
    *,
    referral_id,
    tenant_id,
    organization_id,
    include_deleted: bool = False,
) -> PatientReferral:
    """Retrieve one referral inside the tenant boundary."""

    return get_referral_queryset(
        tenant_id=tenant_id,
        organization_id=organization_id,
        include_deleted=include_deleted,
    ).get(pk=referral_id)


__all__ = (
    "get_referral",
    "get_referral_queryset",
    "list_referrals",
)
