"""
Domain services for Patient Contacts.

Responsibilities
----------------
Services own:

- domain mutation
- normalization
- validation
- persistence
- contact invariants

Services do not own:

- HTTP concerns
- DRF serialization
- RBAC authorization
- workflow orchestration
- domain-event publication

Canonical mutation path:

    API
      |
      v
    Workflow
      |
      v
    Policy
      |
      v
    Service
      |
      v
    Model
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.patient_management.contacts.constants import (
    ContactStatus,
    ContactType,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User


class ContactService:
    """
    Domain service for Patient Contact mutations.

    The public service contract intentionally matches the workflow layer:

        create(
            validated_data=...,
            performed_by=...,
        )

        update(
            instance=...,
            validated_data=...,
            performed_by=...,
        )

        verify(
            instance=...,
            performed_by=...,
        )

    `performed_by` is accepted as part of the canonical mutation contract.
    Audit persistence remains owned by the platform's established audit
    infrastructure and is therefore not duplicated here.
    """

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "created_at",
            "created_by",
            "created_by_id",
            "updated_at",
            "updated_by",
            "updated_by_id",
            "deleted_at",
            "is_deleted",
        }
    )

    # =========================================================================
    # Normalization
    # =========================================================================

    @staticmethod
    def _normalize_data(
        validated_data: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize contact input before persistence.
        """
        normalized = dict(validated_data)

        if "value" in normalized and normalized["value"] is not None:
            value = str(normalized["value"]).strip()

            if not value:
                raise ValidationError(
                    {
                        "value": "Contact value cannot be empty.",
                    }
                )

            normalized["value"] = value

        if normalized.get("contact_type") == ContactType.EMAIL and normalized.get(
            "value"
        ):
            normalized["value"] = normalized["value"].lower()

        return normalized

    # =========================================================================
    # Mutation-field protection
    # =========================================================================

    @classmethod
    def _validate_mutable_fields(
        cls,
        validated_data: Mapping[str, Any],
    ) -> None:
        """
        Reject fields that are never allowed to cross the service boundary
        as mutable application data.
        """
        protected = cls._PROTECTED_FIELDS.intersection(
            validated_data.keys(),
        )

        if protected:
            raise ValidationError(
                dict.fromkeys(
                    sorted(protected),
                    "This field cannot be changed through the contact service.",
                )
            )

    # =========================================================================
    # Organization consistency
    # =========================================================================

    @staticmethod
    def _ensure_patient_organization(
        *,
        contact: Contact,
    ) -> None:
        """
        Ensure the Contact and Patient belong to the same organization.
        """
        patient_organization_id = getattr(
            contact.patient,
            "organization_id",
            None,
        )

        if (
            patient_organization_id is not None
            and patient_organization_id != contact.organization_id
        ):
            raise ValidationError(
                {
                    "organization": (
                        "The contact organization must match the patient organization."
                    )
                }
            )

    # =========================================================================
    # Primary-contact concurrency control
    # =========================================================================

    @staticmethod
    def _lock_patient(
        *,
        patient_id,
    ) -> Patient:
        """
        Lock the owning Patient row.

        All primary-contact mutations use this lock so concurrent requests
        for the same patient serialize correctly.
        """
        return Patient.objects.select_for_update().get(
            pk=patient_id,
        )

    @staticmethod
    def _clear_other_primary_contacts(
        *,
        contact: Contact,
    ) -> None:
        """
        Maintain the single-primary-contact invariant per patient/type.
        """
        (
            Contact.objects.filter(
                patient_id=contact.patient_id,
                contact_type=contact.contact_type,
                is_primary=True,
            )
            .exclude(
                pk=contact.pk,
            )
            .update(
                is_primary=False,
            )
        )

    # =========================================================================
    # Create
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Contact:
        """
        Create a patient contact.

        The organization and patient are expected to have been resolved by
        the workflow before entering the service.
        """
        ContactService._validate_mutable_fields(
            validated_data,
        )

        data = ContactService._normalize_data(
            validated_data,
        )

        if "organization" not in data:
            raise ValidationError(
                {"organization": ("Organization is required to create a contact.")}
            )

        if "patient" not in data:
            raise ValidationError(
                {"patient": ("Patient is required to create a contact.")}
            )

        contact = Contact(
            **data,
        )

        # Ensure the patient relation exists and belongs to the same
        # organization before any primary-contact mutation occurs.
        ContactService._ensure_patient_organization(
            contact=contact,
        )

        if contact.is_primary:
            ContactService._lock_patient(
                patient_id=contact.patient_id,
            )

            ContactService._clear_other_primary_contacts(
                contact=contact,
            )

        contact.full_clean()
        contact.save()

        return contact

    # =========================================================================
    # Update
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Contact,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Contact:
        """
        Update a patient contact.

        Organization and patient ownership are immutable through this
        operation.
        """
        ContactService._validate_mutable_fields(
            validated_data,
        )

        data = ContactService._normalize_data(
            validated_data,
        )

        if not data:
            return instance

        organization_id = instance.organization_id
        patient_id = instance.patient_id
        previous_primary = instance.is_primary

        # A primary mutation or a contact-type change can affect the
        # uniqueness boundary and therefore requires the patient lock.
        primary_boundary_change = (
            "is_primary" in data
            or "contact_type" in data
            or data.get("is_primary") is True
            or previous_primary is True
        )

        if primary_boundary_change:
            ContactService._lock_patient(
                patient_id=patient_id,
            )

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        if instance.organization_id != organization_id:
            raise ValidationError(
                {"organization": ("Contact organization cannot be changed.")}
            )

        if instance.patient_id != patient_id:
            raise ValidationError({"patient": ("Contact patient cannot be changed.")})

        ContactService._ensure_patient_organization(
            contact=instance,
        )

        if instance.is_primary:
            ContactService._clear_other_primary_contacts(
                contact=instance,
            )

        instance.full_clean()
        instance.save()

        return instance

    # =========================================================================
    # Verify
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: Contact,
        performed_by: User | None = None,
    ) -> Contact:
        """
        Mark a contact as verified.
        """
        instance.status = ContactStatus.VERIFIED

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return instance

    # =========================================================================
    # Activate
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: Contact,
        performed_by: User | None = None,
    ) -> Contact:
        """
        Mark a contact as active.
        """
        instance.status = ContactStatus.ACTIVE

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return instance

    # =========================================================================
    # Deactivate
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: Contact,
        performed_by: User | None = None,
    ) -> Contact:
        """
        Mark a contact as inactive.

        An inactive contact cannot remain primary.
        """
        instance.status = ContactStatus.INACTIVE

        # Removing primary status is part of the same atomic mutation.
        instance.is_primary = False

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "is_primary",
                "updated_at",
            ),
        )

        return instance

    # =========================================================================
    # Set Primary
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def set_primary(
        *,
        instance: Contact,
        performed_by: User | None = None,
    ) -> Contact:
        """
        Make the contact primary for its patient and contact type.
        """
        if instance.status == ContactStatus.INACTIVE:
            raise ValidationError(
                {"status": ("An inactive contact cannot be made primary.")}
            )

        ContactService._lock_patient(
            patient_id=instance.patient_id,
        )

        ContactService._clear_other_primary_contacts(
            contact=instance,
        )

        instance.is_primary = True

        instance.full_clean()

        instance.save(
            update_fields=(
                "is_primary",
                "updated_at",
            ),
        )

        return instance

    # =========================================================================
    # Delete
    # =========================================================================

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Contact,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete a patient contact.

        The model's configured delete semantics remain authoritative. This
        service does not bypass the model's persistence lifecycle.
        """
        instance.delete()


# =============================================================================
# Canonical service aliases
# =============================================================================

create_contact = ContactService.create
update_contact = ContactService.update
verify_contact = ContactService.verify
activate_contact = ContactService.activate
deactivate_contact = ContactService.deactivate
set_primary_contact = ContactService.set_primary
delete_contact = ContactService.delete


__all__ = (
    "ContactService",
    "activate_contact",
    "create_contact",
    "deactivate_contact",
    "delete_contact",
    "set_primary_contact",
    "update_contact",
    "verify_contact",
)
