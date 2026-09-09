"""
Patient Address domain model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.core.models import AuditableModel
from apps.patient_management.addresses.constants import (
    AddressSource,
    AddressStatus,
    AddressType,
    AddressUse,
)
from apps.patient_management.addresses.managers import (
    AddressManager,
)
from apps.patient_management.addresses.validators import (
    validate_postal_code,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class Address(AuditableModel):
    """
    Patient address aggregate.

    Organization and patient ownership are immutable through the public
    update workflow. Primary-address uniqueness is enforced both through
    the database constraint and the domain service.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_addresses",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    address_type = models.CharField(
        max_length=20,
        choices=AddressType.choices,
    )

    address_use = models.CharField(
        max_length=20,
        choices=AddressUse.choices,
        default=AddressUse.PRIMARY,
    )

    line_1 = models.CharField(
        max_length=255,
    )

    line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
    )

    country = models.CharField(
        max_length=100,
    )

    postal_code = models.CharField(
        max_length=20,
        validators=(validate_postal_code,),
    )

    status = models.CharField(
        max_length=20,
        choices=AddressStatus.choices,
        default=AddressStatus.ACTIVE,
    )

    source = models.CharField(
        max_length=20,
        choices=AddressSource.choices,
        default=AddressSource.PATIENT,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    objects = AddressManager()

    class Meta:
        ordering = (
            "patient",
            "-is_primary",
            "address_type",
            "created_at",
        )
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "patient",
                    "address_type",
                ),
                condition=Q(
                    is_primary=True,
                ),
                name="uniq_primary_patient_address",
            ),
        )
        indexes = (
            models.Index(
                fields=(
                    "organization",
                    "patient",
                ),
                name="idx_address_org_patient",
            ),
            models.Index(
                fields=(
                    "organization",
                    "address_type",
                ),
                name="idx_address_org_type",
            ),
            models.Index(
                fields=(
                    "organization",
                    "status",
                ),
                name="idx_address_org_status",
            ),
        )

    def clean(self) -> None:
        """
        Validate model-level address invariants.
        """
        super().clean()

        if self.patient_id and self.organization_id:
            patient_organization_id = self.patient.organization_id

            if patient_organization_id != self.organization_id:
                raise ValidationError(
                    {
                        "patient": (
                            "The patient must belong to the selected organization."
                        ),
                    },
                )

        validate_postal_code(
            self.postal_code,
        )

    def __str__(self) -> str:
        return f"{self.line_1}, {self.city}"


__all__ = ("Address",)
