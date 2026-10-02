"""Patient guarantor model."""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class PatientGuarantor(BaseModel):
    """Person or organization financially responsible for a patient."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="patient_guarantors",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="billing_guarantors",
    )
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.JSONField(default=dict, blank=True)
    is_primary = models.BooleanField(default=False, db_index=True)

    class Meta:
        """Database metadata."""

        db_table = "billing_patient_guarantors"
        ordering = ("-is_primary", "name")
        indexes = (
            models.Index(
                fields=("organization", "patient"), name="pguarantor_org_patient_idx"
            ),
            models.Index(
                fields=("patient", "is_primary"), name="pguarantor_patient_primary_idx"
            ),
        )

    def __str__(self) -> str:
        """Return the guarantor display value."""

        return self.name


__all__ = ("PatientGuarantor",)
