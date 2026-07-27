"""
Custom managers for the Patient Documents module.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.patient_documents.querysets import (
    PatientDocumentQuerySet,
)


class PatientDocumentManager(
    models.Manager.from_queryset(
        PatientDocumentQuerySet,
    ),
):
    """
    Default manager for PatientDocument.

    Provides the complete PatientDocumentQuerySet API.
    """


__all__ = ("PatientDocumentManager",)
