"""Canonical Documents media contract over apps.common.storage."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from django.core.exceptions import ValidationError

from apps.common.storage.config import get_storage_client
from apps.common.storage.production import validate_storage_path, validate_upload

MEDIA_TYPES = {
    "pdf": {"application/pdf"},
    "image": {"image/jpeg", "image/png", "image/webp", "image/gif", "image/tiff"},
    "office": {
        "application/msword",
        "application/vnd.ms-excel",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.presentation",
    },
    "audio": {
        "audio/mpeg",
        "audio/mp4",
        "audio/wav",
        "audio/x-wav",
        "audio/ogg",
        "audio/webm",
        "audio/flac",
    },
    "video": {
        "video/mp4",
        "video/webm",
        "video/quicktime",
        "video/x-msvideo",
        "video/mpeg",
        "video/ogg",
    },
}
EXTENSIONS = {
    "pdf": {"pdf"},
    "image": {"jpg", "jpeg", "png", "webp", "gif", "tif", "tiff"},
    "office": {"doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp"},
    "audio": {"mp3", "m4a", "wav", "ogg", "webm", "flac"},
    "video": {"mp4", "webm", "mov", "avi", "mpeg", "mpg", "ogg"},
}


@dataclass(frozen=True, slots=True)
class MediaDescriptor:
    family: str
    original_filename: str
    mime_type: str
    file_size: int
    checksum: str
    storage_key: str


def media_family(*, filename: str, mime_type: str) -> str:
    mime = str(mime_type or "").strip().lower()
    suffix = PurePosixPath(str(filename or "")).suffix.lower().lstrip(".")
    for family, allowed in MEDIA_TYPES.items():
        if mime in allowed:
            if suffix in EXTENSIONS[family]:
                return family
            raise ValidationError("Filename extension is incompatible with MIME type.")
    for family, allowed in EXTENSIONS.items():
        if suffix in allowed:
            return family
    raise ValidationError("Unsupported Documents media type.")


def validate_media(*, filename: str, size: int, mime_type: str) -> str:
    filename = str(filename or "").strip()
    if not filename or "/" in filename or "\\" in filename or chr(0) in filename:
        raise ValidationError("Unsafe or missing filename.")
    if size <= 0:
        raise ValidationError("Media file must not be empty.")
    validate_upload(
        filename=filename, size=size, content_type=str(mime_type or "").strip().lower()
    )
    return media_family(filename=filename, mime_type=mime_type)


def checksum_bytes(content: bytes | bytearray | memoryview) -> str:
    return hashlib.sha256(bytes(content)).hexdigest()


def build_storage_key(
    *,
    tenant_id: Any,
    organization_id: Any,
    document_id: Any,
    filename: str,
    version_number: int,
) -> str:
    if version_number < 1:
        raise ValidationError("Version number must be >= 1.")
    suffix = PurePosixPath(str(filename)).suffix.lower()
    key = f"documents/{tenant_id}/{organization_id}/{document_id}/v{version_number}{suffix}"
    validate_storage_path(key)
    return key


def upload_media(
    *,
    content: bytes | bytearray | memoryview,
    filename: str,
    mime_type: str,
    tenant_id: Any,
    organization_id: Any,
    document_id: Any,
    version_number: int,
    overwrite: bool = False,
) -> MediaDescriptor:
    raw = bytes(content)
    family = validate_media(filename=filename, size=len(raw), mime_type=mime_type)
    key = build_storage_key(
        tenant_id=tenant_id,
        organization_id=organization_id,
        document_id=document_id,
        filename=filename,
        version_number=version_number,
    )
    client = get_storage_client()
    client.upload(key, raw, overwrite=overwrite)
    try:
        stored = client.download(key)
        if len(stored) != len(raw) or checksum_bytes(stored) != checksum_bytes(raw):
            raise ValidationError("Stored media integrity verification failed.")
    except Exception:
        try:
            client.delete(key)
        finally:
            raise
    return MediaDescriptor(
        family=family,
        original_filename=filename.strip(),
        mime_type=str(mime_type).strip().lower(),
        file_size=len(raw),
        checksum=checksum_bytes(raw),
        storage_key=key,
    )


def delete_uploaded_media(*, storage_key: str) -> bool:
    validate_storage_path(storage_key)
    return get_storage_client().delete(storage_key)


def media_url(*, storage_key: str, expires_in: int | None = None) -> str:
    validate_storage_path(storage_key)
    return get_storage_client().url(storage_key, expires_in=expires_in)


def media_exists(*, storage_key: str) -> bool:
    validate_storage_path(storage_key)
    return get_storage_client().exists(storage_key)


__all__ = (
    "MEDIA_TYPES",
    "EXTENSIONS",
    "MediaDescriptor",
    "media_family",
    "validate_media",
    "checksum_bytes",
    "build_storage_key",
    "upload_media",
    "delete_uploaded_media",
    "media_url",
    "media_exists",
)
