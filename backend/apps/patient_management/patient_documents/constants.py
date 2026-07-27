"""
Constants used by the Patient Documents module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import TextChoices


class DocumentCategory(TextChoices):
    """
    Supported patient document categories.
    """

    IDENTITY = "IDENTITY", "Identity"

    INSURANCE = "INSURANCE", "Insurance"

    CONSENT = "CONSENT", "Consent"

    PRESCRIPTION = "PRESCRIPTION", "Prescription"

    LABORATORY = "LABORATORY", "Laboratory"

    RADIOLOGY = "RADIOLOGY", "Radiology"

    PATHOLOGY = "PATHOLOGY", "Pathology"

    CLINICAL = "CLINICAL", "Clinical"

    CARE_PLAN = "CARE_PLAN", "Care Plan"

    OPERATIVE = "OPERATIVE", "Operative Report"

    ADMISSION = "ADMISSION", "Admission"

    DISCHARGE = "DISCHARGE", "Discharge"

    BILLING = "BILLING", "Billing"

    REFERRAL = "REFERRAL", "Referral"

    LEGAL = "LEGAL", "Legal"

    VACCINATION = "VACCINATION", "Vaccination"

    ADVANCE_DIRECTIVE = (
        "ADVANCE_DIRECTIVE",
        "Advance Directive",
    )

    DISABILITY = "DISABILITY", "Disability"

    DEATH = "DEATH", "Death Certificate"

    FINANCIAL = "FINANCIAL", "Financial"

    EXTERNAL_RECORD = (
        "EXTERNAL_RECORD",
        "External Record",
    )

    IMAGE = "IMAGE", "Image"

    VIDEO = "VIDEO", "Video"

    AUDIO = "AUDIO", "Audio"

    OTHER = "OTHER", "Other"


class DocumentStatus(TextChoices):
    """
    Document lifecycle status.
    """

    DRAFT = "DRAFT", "Draft"

    PENDING_REVIEW = (
        "PENDING_REVIEW",
        "Pending Review",
    )

    VERIFIED = "VERIFIED", "Verified"

    ACTIVE = "ACTIVE", "Active"

    REJECTED = "REJECTED", "Rejected"

    ARCHIVED = "ARCHIVED", "Archived"

    EXPIRED = "EXPIRED", "Expired"

    DELETED = "DELETED", "Deleted"


class DocumentVisibility(TextChoices):
    """
    Document visibility level.
    """

    PRIVATE = "PRIVATE", "Private"

    INTERNAL = "INTERNAL", "Internal"

    SHARED = "SHARED", "Shared"

    PUBLIC = "PUBLIC", "Public"


class StorageBackend(TextChoices):
    """
    Storage provider.
    """

    LOCAL = "LOCAL", "Local"

    DATABASE = "DATABASE", "Database"

    S3 = "S3", "Amazon S3"

    AZURE = "AZURE", "Azure Blob Storage"

    GCS = "GCS", "Google Cloud Storage"

    MINIO = "MINIO", "MinIO"


class DocumentAction(TextChoices):
    """
    Supported document audit actions.
    """

    CREATED = "CREATED", "Created"

    UPDATED = "UPDATED", "Updated"

    UPLOADED = "UPLOADED", "Uploaded"

    VIEWED = "VIEWED", "Viewed"

    DOWNLOADED = "DOWNLOADED", "Downloaded"

    PRINTED = "PRINTED", "Printed"

    SHARED = "SHARED", "Shared"

    VERIFIED = "VERIFIED", "Verified"

    REJECTED = "REJECTED", "Rejected"

    EXPORTED = "EXPORTED", "Exported"

    ARCHIVED = "ARCHIVED", "Archived"

    RESTORED = "RESTORED", "Restored"

    DELETED = "DELETED", "Deleted"


class DocumentSource(TextChoices):
    """
    Source from which the document originated.
    """

    MANUAL = "MANUAL", "Manual Upload"

    SCANNER = "SCANNER", "Scanner"

    LABORATORY = "LABORATORY", "Laboratory"

    RADIOLOGY = "RADIOLOGY", "Radiology"

    PATHOLOGY = "PATHOLOGY", "Pathology"

    PHARMACY = "PHARMACY", "Pharmacy"

    CLINICAL = "CLINICAL", "Clinical"

    BILLING = "BILLING", "Billing"

    INSURANCE = "INSURANCE", "Insurance"

    PATIENT_PORTAL = (
        "PATIENT_PORTAL",
        "Patient Portal",
    )

    MOBILE_APP = "MOBILE_APP", "Mobile App"

    API = "API", "API"

    IMPORT = "IMPORT", "Import"

    MIGRATION = "MIGRATION", "Migration"

    AI = "AI", "AI Generated"


DEFAULT_DOCUMENT_CATEGORY: Final = DocumentCategory.OTHER

DEFAULT_DOCUMENT_STATUS: Final = DocumentStatus.DRAFT

DEFAULT_DOCUMENT_VISIBILITY: Final = DocumentVisibility.PRIVATE

DEFAULT_STORAGE_BACKEND: Final = StorageBackend.LOCAL

DEFAULT_DOCUMENT_SOURCE: Final = DocumentSource.MANUAL


__all__ = (
    "DEFAULT_DOCUMENT_CATEGORY",
    "DEFAULT_DOCUMENT_SOURCE",
    "DEFAULT_DOCUMENT_STATUS",
    "DEFAULT_DOCUMENT_VISIBILITY",
    "DEFAULT_STORAGE_BACKEND",
    "DocumentAction",
    "DocumentCategory",
    "DocumentSource",
    "DocumentStatus",
    "DocumentVisibility",
    "StorageBackend",
)
