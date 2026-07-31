"""
Charge Capture selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.charge_capture.models import ChargeCapture


class ChargeCaptureSelector:
    """
    Read-only queries for charge capture records.
    """

    @staticmethod
    def queryset() -> QuerySet[ChargeCapture]:
        return ChargeCapture.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        charge_id: UUID,
    ) -> ChargeCapture:
        return get_object_or_404(
            ChargeCaptureSelector.queryset(),
            pk=charge_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ChargeCapture]:
        return ChargeCaptureSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ChargeCapture]:
        return ChargeCaptureSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ChargeCaptureSelector",
]
