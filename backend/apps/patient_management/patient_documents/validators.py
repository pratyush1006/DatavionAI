"""
Validators for the Patient Documents module.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from apps.patient_management.patient_documents.constants import (
    DocumentCategory,
)

# 100 MB
MAX_DOCUMENT_SIZE = 100 * 1024 * 1024


ALLOWED_EXTENSIONS: dict[str, set[str]] = {
    DocumentCategory.IDENTITY: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    },
    DocumentCategory.INSURANCE: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    },
    DocumentCategory.CONSENT: {
        ".pdf",
    },
    DocumentCategory.PRESCRIPTION: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    },
    DocumentCategory.LABORATORY: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    },
    DocumentCategory.RADIOLOGY: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".dcm",
    },
    DocumentCategory.PATHOLOGY: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    },
    DocumentCategory.CLINICAL: {
        ".pdf",
        ".doc",
        ".docx",
    },
    DocumentCategory.IMAGE: {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    },
    DocumentCategory.VIDEO: {
        ".mp4",
        ".mov",
        ".avi",
    },
    DocumentCategory.AUDIO: {
        ".mp3",
        ".wav",
    },
    DocumentCategory.OTHER: {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".doc",
        ".docx",
        ".xlsx",
        ".csv",
        ".txt",
    },
}


def validate_document_file(
    file: UploadedFile,
) -> None:
    """
    Validate uploaded document file.
    """

    if file.size > MAX_DOCUMENT_SIZE:
        raise ValidationError(
            "Document exceeds the maximum allowed size (100 MB).",
        )


def validate_document_extension(
    *,
    file: UploadedFile,
    category: str,
) -> None:
    """
    Validate document extension against category.
    """

    extension = Path(file.name).suffix.lower()

    allowed = ALLOWED_EXTENSIONS.get(
        category,
        ALLOWED_EXTENSIONS[DocumentCategory.OTHER],
    )

    if extension not in allowed:
        raise ValidationError(
            f"'{extension}' files are not allowed for '{category}'.",
        )


def validate_content_type(
    file: UploadedFile,
) -> None:
    """
    Validate MIME type.
    """

    guessed_type, _ = mimetypes.guess_type(
        file.name,
    )

    if guessed_type is None:
        raise ValidationError(
            "Unable to determine document type.",
        )


def validate_patient_document(
    *,
    file: UploadedFile,
    category: str,
) -> None:
    """
    Run all patient document validations.
    """

    validate_document_file(
        file,
    )

    validate_document_extension(
        file=file,
        category=category,
    )

    validate_content_type(
        file,
    )


__all__ = (
    "ALLOWED_EXTENSIONS",
    "MAX_DOCUMENT_SIZE",
    "validate_content_type",
    "validate_document_extension",
    "validate_document_file",
    "validate_patient_document",
)
