"""
Shared storage utilities.
"""

from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path
from uuid import uuid4


def calculate_checksum(
    file,
    algorithm: str = "sha256",
) -> str:
    """
    Calculate the checksum of a file.
    """

    digest = hashlib.new(
        algorithm,
    )

    for chunk in file.chunks():
        digest.update(
            chunk,
        )

    file.seek(0)

    return digest.hexdigest()


def guess_content_type(
    filename: str,
) -> str:
    """
    Guess the MIME type from a filename.
    """

    content_type, _ = mimetypes.guess_type(
        filename,
    )

    return content_type or "application/octet-stream"


def sanitize_filename(
    filename: str,
) -> str:
    """
    Return a safe filename.
    """

    return Path(
        filename,
    ).name


def generate_storage_path(
    *,
    organization_id,
    patient_id,
    filename: str,
) -> str:
    """
    Generate a deterministic storage path.
    """

    filename = sanitize_filename(
        filename,
    )

    return f"{organization_id}/{patient_id}/{uuid4()}_{filename}"


__all__ = [
    "calculate_checksum",
    "generate_storage_path",
    "guess_content_type",
    "sanitize_filename",
]
