"""
Asset upload service.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

from django.db import transaction

from apps.storage.constants import (
    ASSET_STATUS_READY,
)
from apps.storage.models import (
    Asset,
    Folder,
)
from apps.storage.providers.local import LocalStorageProvider


@transaction.atomic
def upload_asset(
    *,
    organization,
    uploaded_by,
    file: BinaryIO,
    original_name: str,
    mime_type: str,
    category: str,
    folder: Folder | None = None,
    visibility: str,
    provider=None,
) -> Asset:
    """
    Upload an asset and create its metadata.
    """

    provider = provider or LocalStorageProvider()

    extension = Path(original_name).suffix.lower().lstrip(".")

    storage_key = f"{organization.id}/{uuid4().hex}.{extension}"

    storage_path = provider.upload(
        file=file,
        storage_key=storage_key,
        content_type=mime_type,
    )

    return Asset.objects.create(
        organization=organization,
        uploaded_by=uploaded_by,
        folder=folder,
        name=Path(original_name).stem,
        original_name=original_name,
        extension=extension,
        mime_type=mime_type,
        category=category,
        size=getattr(file, "size", 0),
        provider=provider.__class__.__name__,
        storage_key=storage_key,
        path=storage_path,
        checksum="",
        visibility=visibility,
        status=ASSET_STATUS_READY,
    )
