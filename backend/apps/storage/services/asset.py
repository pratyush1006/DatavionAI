"""
Asset services.
"""

from __future__ import annotations

from django.db import transaction

from apps.storage.models import Asset


@transaction.atomic
def update_asset(
    *,
    asset: Asset,
    **fields,
) -> Asset:
    """
    Update asset metadata.
    """

    for field, value in fields.items():
        setattr(
            asset,
            field,
            value,
        )

    asset.save(
        update_fields=[
            *fields.keys(),
            "updated_at",
        ],
    )

    return asset


@transaction.atomic
def move_asset(
    *,
    asset: Asset,
    folder,
) -> Asset:
    """
    Move an asset to another folder.
    """

    asset.folder = folder

    asset.save(
        update_fields=[
            "folder",
            "updated_at",
        ],
    )

    return asset


@transaction.atomic
def change_asset_visibility(
    *,
    asset: Asset,
    visibility: str,
) -> Asset:
    """
    Change asset visibility.
    """

    asset.visibility = visibility

    asset.save(
        update_fields=[
            "visibility",
            "updated_at",
        ],
    )

    return asset


@transaction.atomic
def change_asset_status(
    *,
    asset: Asset,
    status: str,
) -> Asset:
    """
    Change asset status.
    """

    asset.status = status

    asset.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return asset
