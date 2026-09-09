"""Domain services for patient document versions."""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.patient_documents.constants import (
    DocumentVersionStatus,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
    PatientDocumentVersion,
)


class PatientDocumentVersionService:
    """Create immutable version metadata records."""

    @staticmethod
    @transaction.atomic
    def create(
        *,
        patient_document,
        storage_key: str,
        performed_by,
        original_filename: str = "",
        mime_type: str = "",
        file_size: int = 0,
        checksum: str = "",
        notes: str = "",
    ) -> PatientDocumentVersion:
        """Create the next sequential version."""
        parent_document = PatientDocument.objects.select_for_update().get(
            pk=patient_document.pk,
        )

        latest = (
            PatientDocumentVersion.objects.select_for_update()
            .filter(
                patient_document=patient_document,
            )
            .order_by(
                "-version_number",
            )
            .first()
        )

        next_number = latest.version_number + 1 if latest is not None else 1

        PatientDocumentVersion.objects.filter(
            patient_document=patient_document,
            status=DocumentVersionStatus.ACTIVE,
        ).update(
            status=DocumentVersionStatus.SUPERSEDED,
        )

        return PatientDocumentVersion.objects.create(
            patient_document=patient_document,
            version_number=next_number,
            storage_key=storage_key,
            original_filename=original_filename,
            mime_type=mime_type,
            file_size=file_size,
            checksum=checksum,
            status=DocumentVersionStatus.ACTIVE,
            notes=notes,
            created_by=performed_by,
        )


__all__ = ("PatientDocumentVersionService",)
