"""Patient guarantor selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.billing.patient_billing.models import PatientGuarantor


class PatientGuarantorSelector:
    """Provide organization-scoped guarantor reads."""

    @staticmethod
    def queryset(*, organization_id: UUID) -> QuerySet[PatientGuarantor]:
        """Return organization-scoped guarantors."""

        return PatientGuarantor.objects.select_related(
            "patient", "organization"
        ).filter(
            organization_id=organization_id,
        )

    @staticmethod
    def get(*, organization_id: UUID, guarantor_id: UUID) -> PatientGuarantor:
        """Return one organization-scoped guarantor."""

        return PatientGuarantorSelector.queryset(organization_id=organization_id).get(
            id=guarantor_id
        )


__all__ = ("PatientGuarantorSelector",)
