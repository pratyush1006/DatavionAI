"""
Asset deletion service.
"""

from __future__ import annotations

from django.db import transaction

from apps.storage.constants import (
    ASSET_STATUS_DELETED,
)
from apps.storage.models import Asset
from apps.storage.providers.base import BaseStorageProvider
from apps.storage.providers.local import LocalStorageProvider


@transaction.atomic
def delete_asset(
    *,
    asset: Asset,
    provider: BaseStorageProvider | None = None,
) -> Asset:
    """
    Delete an asset from storage and mark it as deleted.
    """

    provider = provider or LocalStorageProvider()

    if provider.exists(
        storage_key=asset.storage_key,
    ):
        provider.delete(
            storage_key=asset.storage_key,
        )

    asset.status = ASSET_STATUS_DELETED
    asset.is_active = False

    asset.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return asset
