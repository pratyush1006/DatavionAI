"""Patient billing account selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.revenue_cycle.billing.patient_billing.models import PatientBillingAccount


class PatientBillingAccountSelector:
    """Provide tenant-safe patient billing account reads."""

    @staticmethod
    def queryset(*, organization_id: UUID) -> QuerySet[PatientBillingAccount]:
        """Return active, organization-scoped accounts."""

        return PatientBillingAccount.objects.select_related(
            "organization", "patient"
        ).filter(
            organization_id=organization_id,
        )

    @staticmethod
    def get(*, organization_id: UUID, account_id: UUID) -> PatientBillingAccount:
        """Return one organization-scoped account."""

        return PatientBillingAccountSelector.queryset(
            organization_id=organization_id
        ).get(id=account_id)

    @staticmethod
    def by_patient(
        *, organization_id: UUID, patient_id: UUID
    ) -> PatientBillingAccount | None:
        """Return a patient's billing account when present."""

        return (
            PatientBillingAccountSelector.queryset(organization_id=organization_id)
            .filter(
                patient_id=patient_id,
            )
            .first()
        )


__all__ = ("PatientBillingAccountSelector",)
