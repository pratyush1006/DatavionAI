"""Query managers for medical history."""

from __future__ import annotations

from uuid import UUID

from django.db import models

from apps.patient_management.medical_history.constants import ClinicalStatus


class MedicalHistoryQuerySet(models.QuerySet):
    """MedicalHistoryQuerySet implementation."""

    def active(self):
        """Active."""
        return self.filter(is_deleted=False, is_active=True)

    def inactive(self):
        """Inactive."""
        return self.filter(is_deleted=False, is_active=False)

    def for_patient(self, patient_id: UUID):
        """For patient."""
        return self.filter(patient_id=patient_id, is_deleted=False)

    def for_organization(self, organization_id: UUID):
        """For organization."""
        return self.filter(organization_id=organization_id, is_deleted=False)

    def by_type(self, history_type: str):
        """By type."""
        return self.filter(history_type=history_type, is_deleted=False)

    def current(self):
        """Current."""
        return self.filter(is_deleted=False, clinical_status=ClinicalStatus.ACTIVE)

    def with_relations(self):
        """With relations."""
        return self.select_related("organization", "patient", "verified_by")


class MedicalHistoryManager(models.Manager.from_queryset(MedicalHistoryQuerySet)):
    """MedicalHistoryManager implementation."""

    def get_queryset(self):
        """Get queryset."""
        return super().get_queryset().filter(is_deleted=False)


__all__ = (
    "MedicalHistoryQuerySet",
    "MedicalHistoryManager",
)
