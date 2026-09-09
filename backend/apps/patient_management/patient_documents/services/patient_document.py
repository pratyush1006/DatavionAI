"""Domain services for Patient Documents."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.patient_documents.constants import (
    DOCUMENT_STATUS_TRANSITIONS,
    PatientDocumentStatus,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.validators import (
    validate_document_data,
)


class PatientDocumentService:
    """Perform transactional Patient Document mutations."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        organization,
        patient,
        title: str,
        storage_key: str,
        performed_by,
        category: str,
        description: str = "",
        original_filename: str = "",
        mime_type: str = "",
        file_size: int = 0,
        checksum: str = "",
        is_confidential: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> PatientDocument:
        """Create a new patient document."""
        if organization.tenant_id != patient.organization.tenant_id:
            raise ValidationError(
                "Patient and organization must belong to the same tenant.",
            )

        if patient.organization_id != organization.id:
            raise ValidationError(
                "Patient and organization must match.",
            )

        if not title.strip():
            raise ValidationError(
                "Document title is required.",
            )

        if not storage_key.strip():
            raise ValidationError(
                "Storage key is required.",
            )

        return PatientDocument.objects.create(
            organization=organization,
            patient=patient,
            title=title.strip(),
            category=category,
            status=PatientDocumentStatus.DRAFT,
            description=description.strip(),
            original_filename=original_filename.strip(),
            storage_key=storage_key.strip(),
            mime_type=mime_type.strip(),
            file_size=file_size,
            checksum=checksum.strip(),
            is_confidential=is_confidential,
            metadata=metadata or {},
            created_by=performed_by,
        )

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: PatientDocument,
        validated_data: Mapping[str, Any],
        performed_by,
    ) -> PatientDocument:
        """Update mutable document metadata."""
        validate_document_data(
            validated_data,
        )

        data = dict(validated_data)
        data.pop(
            "organization",
            None,
        )
        data.pop(
            "patient",
            None,
        )

        for field_name, value in data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(
                instance,
                field_name,
                value,
            )

        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: PatientDocument,
        performed_by,
    ) -> PatientDocument:
        """Activate a draft or archived patient document."""
        if instance.is_deleted:
            raise ValidationError(
                "A deleted document cannot be activated.",
            )

        allowed = DOCUMENT_STATUS_TRANSITIONS.get(
            instance.status,
            frozenset(),
        )
        if PatientDocumentStatus.ACTIVE not in allowed:
            raise ValidationError(
                f"Document cannot transition from '{instance.status}' to "
                f"'{PatientDocumentStatus.ACTIVE}'.",
            )

        instance.status = PatientDocumentStatus.ACTIVE
        instance.is_active = True
        if instance.uploaded_at is None:
            instance.uploaded_at = timezone.now()
        instance.save(
            update_fields=[
                "status",
                "is_active",
                "uploaded_at",
                "updated_at",
            ],
        )
        return instance

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: PatientDocument,
        performed_by,
    ) -> PatientDocument:
        """Archive an active patient document."""
        if instance.is_deleted:
            raise ValidationError(
                "A deleted document cannot be archived.",
            )

        allowed = DOCUMENT_STATUS_TRANSITIONS.get(
            instance.status,
            frozenset(),
        )
        if PatientDocumentStatus.ARCHIVED not in allowed:
            raise ValidationError(
                f"Document cannot transition from '{instance.status}' to "
                f"'{PatientDocumentStatus.ARCHIVED}'.",
            )

        instance.status = PatientDocumentStatus.ARCHIVED
        instance.is_active = False
        instance.archived_at = timezone.now()
        instance.save(
            update_fields=[
                "status",
                "is_active",
                "archived_at",
                "updated_at",
            ],
        )
        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: PatientDocument,
        performed_by,
    ) -> PatientDocument:
        """Soft-delete a patient document."""
        instance.delete(
            user_id=performed_by.pk,
        )
        return instance

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: PatientDocument,
        performed_by,
    ) -> PatientDocument:
        """Restore a soft-deleted patient document."""
        instance.restore()
        instance.status = PatientDocumentStatus.ACTIVE
        instance.is_active = True
        instance.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
                "status",
                "is_active",
                "updated_at",
            ],
        )
        return instance


__all__ = ("PatientDocumentService",)
