"""
Asset download service.
"""

from __future__ import annotations

from typing import BinaryIO

from apps.storage.models import Asset
from apps.storage.providers.base import BaseStorageProvider
from apps.storage.providers.local import LocalStorageProvider


def download_asset(
    *,
    asset: Asset,
    provider: BaseStorageProvider | None = None,
) -> BinaryIO:
    """
    Download an asset from the configured storage provider.
    """

    provider = provider or LocalStorageProvider()

    return provider.download(
        storage_key=asset.storage_key,
    )


def get_asset_url(
    *,
    asset: Asset,
    provider: BaseStorageProvider | None = None,
    expires_in: int | None = None,
) -> str:
    """
    Return the access URL for an asset.
    """

    provider = provider or LocalStorageProvider()

    return provider.url(
        storage_key=asset.storage_key,
        expires_in=expires_in,
    )
