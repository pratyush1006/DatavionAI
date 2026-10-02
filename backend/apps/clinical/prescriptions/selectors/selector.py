"""Organization-scoped selectors for Prescription."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.clinical.prescriptions.models import Prescription


class PrescriptionSelector:
    @staticmethod
    def queryset(*, organization_id: UUID) -> QuerySet:
        return Prescription.objects.filter(organization_id=organization_id)

    @classmethod
    def get(cls, *, organization_id: UUID, record_id: UUID) -> Prescription:
        return cls.queryset(organization_id=organization_id).get(pk=record_id)

    @classmethod
    def list(cls, *, organization_id: UUID) -> QuerySet:
        return cls.queryset(organization_id=organization_id)


__all__ = ("PrescriptionSelector",)
