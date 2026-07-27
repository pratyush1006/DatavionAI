"""
Factories for Patient Documents tests.
"""

from __future__ import annotations

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


def create_patient_document(
    **kwargs,
) -> PatientDocument:
    """
    Create a PatientDocument for testing.
    """

    defaults = {
        "organization": kwargs.pop("organization"),
        "patient": kwargs.pop("patient"),
        "document_number": kwargs.pop(
            "document_number",
            "DOC-000001",
        ),
        "title": kwargs.pop(
            "title",
            "Laboratory Report",
        ),
        "description": kwargs.pop(
            "description",
            "",
        ),
        "category": kwargs.pop(
            "category",
            "LABORATORY",
        ),
        "source": kwargs.pop(
            "source",
            "MANUAL",
        ),
        "status": kwargs.pop(
            "status",
            "ACTIVE",
        ),
        "visibility": kwargs.pop(
            "visibility",
            "PRIVATE",
        ),
        "storage_backend": kwargs.pop(
            "storage_backend",
            "LOCAL",
        ),
        "current_version": kwargs.pop(
            "current_version",
            1,
        ),
        "tags": kwargs.pop(
            "tags",
            [],
        ),
    }

    defaults.update(kwargs)

    return PatientDocument.objects.create(
        **defaults,
    )
