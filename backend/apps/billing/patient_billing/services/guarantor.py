"""Patient guarantor domain services.

The service layer owns guarantor aggregate locking and primary-guarantor
consistency for Patient Billing.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.billing.patient_billing.exceptions import PatientBillingOrganizationError
from apps.billing.patient_billing.models import PatientGuarantor
from apps.patient_management.patients.models import Patient


class PatientGuarantorService:
    """Execute transactional guarantor mutations."""

    @staticmethod
    def _lock_patient(
        *,
        organization_id: UUID,
        patient_id: UUID,
    ) -> Patient:
        """Lock the canonical Patient aggregate within the organization."""

        return Patient.objects.select_for_update().get(
            id=patient_id,
            organization_id=organization_id,
        )

    @staticmethod
    def _set_primary(
        *,
        organization_id: UUID,
        patient_id: UUID,
        guarantor_id: UUID,
    ) -> None:
        """Make one guarantor primary after serializing on the Patient row."""

        PatientGuarantor.objects.filter(
            organization_id=organization_id,
            patient_id=patient_id,
        ).exclude(
            id=guarantor_id,
        ).update(
            is_primary=False,
        )

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization: Any,
        patient: Any,
        validated_data: Mapping[str, Any],
    ) -> PatientGuarantor:
        """Create an organization-owned guarantor with aggregate locking."""

        if patient.organization_id != organization.id:
            raise PatientBillingOrganizationError(
                "Patient does not belong to the billing organization.",
            )
        locked_patient = PatientGuarantorService._lock_patient(
            organization_id=organization.id,
            patient_id=patient.id,
        )
        guarantor = PatientGuarantor(
            organization=organization,
            patient=locked_patient,
            **validated_data,
        )
        guarantor.full_clean()
        guarantor.save()
        if guarantor.is_primary:
            PatientGuarantorService._set_primary(
                organization_id=organization.id,
                patient_id=locked_patient.id,
                guarantor_id=guarantor.id,
            )
        return guarantor

    @staticmethod
    @transaction.atomic
    def update(
        *,
        organization_id: UUID,
        instance: PatientGuarantor,
        validated_data: Mapping[str, Any],
    ) -> PatientGuarantor:
        """Update a guarantor while serializing primary changes on Patient."""

        locked_instance = PatientGuarantor.objects.select_for_update().get(
            id=instance.id,
            organization_id=organization_id,
        )
        locked_patient = PatientGuarantorService._lock_patient(
            organization_id=organization_id,
            patient_id=locked_instance.patient_id,
        )
        for field in (
            "name",
            "relationship",
            "phone",
            "email",
            "address",
            "is_primary",
        ):
            if field in validated_data:
                setattr(locked_instance, field, validated_data[field])
        locked_instance.patient = locked_patient
        locked_instance.full_clean()
        locked_instance.save()
        if locked_instance.is_primary:
            PatientGuarantorService._set_primary(
                organization_id=organization_id,
                patient_id=locked_patient.id,
                guarantor_id=locked_instance.id,
            )
        return locked_instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        organization_id: UUID,
        instance: PatientGuarantor,
        user_id: Any = None,
    ) -> PatientGuarantor:
        """Soft-delete a guarantor inside its organization."""

        guarantor = PatientGuarantor.objects.select_for_update().get(
            id=instance.id,
            organization_id=organization_id,
        )
        PatientGuarantorService._lock_patient(
            organization_id=organization_id,
            patient_id=guarantor.patient_id,
        )
        guarantor.delete(user_id=user_id)
        return guarantor

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        organization_id: UUID,
        guarantor_id: UUID,
    ) -> PatientGuarantor:
        """Restore a guarantor while preserving primary-guarantor consistency."""

        guarantor = PatientGuarantor.all_objects.select_for_update().get(
            id=guarantor_id,
            organization_id=organization_id,
            is_deleted=True,
        )
        locked_patient = PatientGuarantorService._lock_patient(
            organization_id=organization_id,
            patient_id=guarantor.patient_id,
        )
        guarantor.restore()
        if guarantor.is_primary:
            PatientGuarantorService._set_primary(
                organization_id=organization_id,
                patient_id=locked_patient.id,
                guarantor_id=guarantor.id,
            )
        return guarantor


__all__ = ("PatientGuarantorService",)
