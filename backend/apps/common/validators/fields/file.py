"""
Reusable file validators.

Provides reusable validation utilities for uploaded files used
throughout DatavionOS.
"""

from __future__ import annotations

from collections.abc import Collection

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

DEFAULT_FILE_SIZE_MESSAGE = "The uploaded file exceeds the maximum allowed size."

DEFAULT_FILE_EXTENSION_MESSAGE = "The uploaded file type is not allowed."

DEFAULT_FILE_CONTENT_TYPE_MESSAGE = "The uploaded file content type is not allowed."


def validate_file_size(
    file: UploadedFile,
    *,
    max_size: int,
) -> None:
    """
    Validate uploaded file size.
    """

    if file.size > max_size:
        raise ValidationError(
            DEFAULT_FILE_SIZE_MESSAGE,
        )


def file_size_validator(
    *,
    max_size: int,
):
    """
    Create reusable file size validator.
    """

    def validator(
        file: UploadedFile,
    ) -> None:
        validate_file_size(
            file,
            max_size=max_size,
        )

    return validator


def validate_file_extension(
    file: UploadedFile,
    *,
    allowed_extensions: Collection[str],
) -> None:
    """
    Validate uploaded file extension.
    """

    extension = file.name.rsplit(
        ".",
        1,
    )

    if len(extension) != 2:
        raise ValidationError(
            DEFAULT_FILE_EXTENSION_MESSAGE,
        )

    suffix = extension[1].lower()

    normalized = {ext.lower().lstrip(".") for ext in allowed_extensions}

    if suffix not in normalized:
        raise ValidationError(
            DEFAULT_FILE_EXTENSION_MESSAGE,
        )


def file_extension_validator(
    allowed_extensions: Collection[str],
):
    """
    Create reusable file extension validator.
    """

    def validator(
        file: UploadedFile,
    ) -> None:
        validate_file_extension(
            file,
            allowed_extensions=allowed_extensions,
        )

    return validator


def validate_content_type(
    file: UploadedFile,
    *,
    allowed_content_types: Collection[str],
) -> None:
    """
    Validate uploaded file content type.
    """

    if file.content_type not in allowed_content_types:
        raise ValidationError(
            DEFAULT_FILE_CONTENT_TYPE_MESSAGE,
        )


def content_type_validator(
    allowed_content_types: Collection[str],
):
    """
    Create reusable content type validator.
    """

    def validator(
        file: UploadedFile,
    ) -> None:
        validate_content_type(
            file,
            allowed_content_types=allowed_content_types,
        )

    return validator


__all__ = (
    "DEFAULT_FILE_CONTENT_TYPE_MESSAGE",
    "DEFAULT_FILE_EXTENSION_MESSAGE",
    "DEFAULT_FILE_SIZE_MESSAGE",
    "content_type_validator",
    "file_extension_validator",
    "file_size_validator",
    "validate_content_type",
    "validate_file_extension",
    "validate_file_size",
)
