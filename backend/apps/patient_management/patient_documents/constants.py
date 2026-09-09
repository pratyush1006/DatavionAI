"""Constants and lifecycle choices for Patient Documents."""

from __future__ import annotations

from django.db import models


class PatientDocumentStatus(models.TextChoices):
    """Lifecycle states for a patient document."""

    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


class PatientDocumentCategory(models.TextChoices):
    """Clinical and administrative categories for patient documents."""

    MEDICAL_RECORD = "medical_record", "Medical Record"
    LAB_RESULT = "lab_result", "Laboratory Result"
    IMAGING = "imaging", "Imaging"
    PRESCRIPTION = "prescription", "Prescription"
    INSURANCE = "insurance", "Insurance"
    CONSENT = "consent", "Consent"
    REFERRAL = "referral", "Referral"
    IDENTIFICATION = "identification", "Identification"
    ADMINISTRATIVE = "administrative", "Administrative"
    OTHER = "other", "Other"


class DocumentVersionStatus(models.TextChoices):
    """Lifecycle states for a document version."""

    ACTIVE = "active", "Active"
    SUPERSEDED = "superseded", "Superseded"


DOCUMENT_STATUS_TRANSITIONS = {
    "draft": frozenset(
        {
            "active",
        }
    ),
    "active": frozenset(
        {
            "archived",
        }
    ),
    "archived": frozenset(
        {
            "active",
        }
    ),
}


class DocumentAccessAction(models.TextChoices):
    """Audited access operations against patient documents."""

    VIEW = "view", "View"
    DOWNLOAD = "download", "Download"
    PREVIEW = "preview", "Preview"
    SHARE = "share", "Share"


__all__ = (
    "DocumentAccessAction",
    "DocumentVersionStatus",
    "PatientDocumentCategory",
    "PatientDocumentStatus",
)
