from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import PurePosixPath

from django.conf import settings

PRODUCTION_ENVIRONMENTS = frozenset({"production", "prod", "staging", "stage"})
LOCAL_BACKENDS = frozenset({"django.core.files.storage.FileSystemStorage"})
MAX_STORAGE_UPLOAD_BYTES = int(
    os.environ.get("DATAVION_STORAGE_MAX_UPLOAD_BYTES", str(25 * 1024 * 1024))
)
ALLOWED_UPLOAD_EXTENSIONS = frozenset(
    x.strip().lower().lstrip(".")
    for x in os.environ.get(
        "DATAVION_STORAGE_ALLOWED_EXTENSIONS",
        "pdf,jpg,jpeg,png,webp,gif,tif,tiff,csv,txt,json,xml,doc,docx,xls,xlsx,ppt,pptx,odt,ods,odp,mp3,m4a,wav,ogg,flac,webm,mp4,mov,avi,mpeg,mpg",
    ).split(",")
    if x.strip()
)


@dataclass(frozen=True)
class StorageReadiness:
    environment: str
    backend: str
    configured: bool
    production_safe: bool
    path_safe: bool
    upload_policy_ready: bool
    health_probe_available: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def _environment() -> str:
    return (
        str(
            getattr(settings, "DATAVION_ENVIRONMENT", None)
            or os.environ.get("DATAVION_ENVIRONMENT", "")
            or ("development" if getattr(settings, "DEBUG", False) else "production")
        )
        .strip()
        .lower()
    )


def configured_backend() -> str:
    storages = getattr(settings, "STORAGES", {}) or {}
    if isinstance(storages, dict):
        default = storages.get("default", {})
        if isinstance(default, dict) and default.get("BACKEND"):
            return str(default["BACKEND"]).strip()
    return str(getattr(settings, "DEFAULT_FILE_STORAGE", "") or "").strip()


def _options() -> dict:
    storages = getattr(settings, "STORAGES", {}) or {}
    default = storages.get("default", {}) if isinstance(storages, dict) else {}
    options = default.get("OPTIONS", {}) if isinstance(default, dict) else {}
    return options if isinstance(options, dict) else {}


def validate_storage_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Storage path must be a non-empty string.")
    value = path.replace("\\", "/").strip()
    if value.startswith("/") or (len(value) >= 2 and value[1] == ":"):
        raise ValueError("Absolute or drive-qualified storage paths are not allowed.")
    if "\x00" in value:
        raise ValueError("NUL bytes are not allowed.")
    parts = PurePosixPath(value).parts
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("Unsafe storage path.")
    return "/".join(parts)


def validate_upload(
    filename: str, size: int, *, content_type: str | None = None
) -> None:
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Filename is required.")
    if size < 0 or size > MAX_STORAGE_UPLOAD_BYTES:
        raise ValueError("Upload size violates the configured storage limit.")
    name = filename.replace("\\", "/").split("/")[-1]
    if not name or name in {".", ".."} or "\x00" in name:
        raise ValueError("Unsafe filename.")
    extension = name.rsplit(".", 1)[1].lower() if "." in name else ""
    if ALLOWED_UPLOAD_EXTENSIONS and extension not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError(f"File extension '.{extension}' is not permitted.")
    if content_type is not None and (
        not isinstance(content_type, str) or not content_type.strip()
    ):
        raise ValueError("Content type must be non-empty when provided.")


def storage_readiness(*, perform_probe: bool = False) -> StorageReadiness:
    environment = _environment()
    backend = configured_backend()
    errors: list[str] = []
    warnings: list[str] = []
    configured = bool(backend)
    if not configured:
        errors.append("No default storage backend is configured.")
    production_safe = configured
    if environment in PRODUCTION_ENVIRONMENTS and backend in LOCAL_BACKENDS:
        production_safe = False
        errors.append("Local FileSystemStorage is not approved for production.")
    upload_policy_ready = MAX_STORAGE_UPLOAD_BYTES > 0 and bool(
        ALLOWED_UPLOAD_EXTENSIONS
    )
    if not upload_policy_ready:
        errors.append("Storage upload policy is not configured.")
    if backend and backend not in LOCAL_BACKENDS and not _options():
        warnings.append(
            "Verify production provider credentials, bucket/container and endpoint are supplied by deployment configuration."
        )
    if perform_probe and configured:
        try:
            from django.core.files.base import ContentFile
            from django.core.files.storage import default_storage

            probe = "datavionos/health/.storage_probe"
            default_storage.save(probe, ContentFile(b"datavion-storage-probe"))
            if not default_storage.exists(probe):
                errors.append("Storage probe object was not found after write.")
            default_storage.delete(probe)
        except Exception as exc:
            errors.append(f"Storage I/O probe failed: {exc.__class__.__name__}: {exc}")
    return StorageReadiness(
        environment,
        backend,
        configured,
        production_safe,
        True,
        upload_policy_ready,
        True,
        tuple(errors),
        tuple(warnings),
    )


def storage_is_ready(*, perform_probe: bool = False) -> bool:
    result = storage_readiness(perform_probe=perform_probe)
    return (
        result.configured
        and result.production_safe
        and result.path_safe
        and result.upload_policy_ready
        and not result.errors
    )
