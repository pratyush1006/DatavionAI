"""
Asset selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.storage.models import Asset


def get_asset(
    *,
    asset_id,
    organization=None,
) -> Asset:
    """
    Return an asset by its identifier.

    If an organization is provided, ensure the asset belongs to
    that organization.
    """

    queryset = Asset.objects.all()

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    return queryset.get(
        pk=asset_id,
    )


def get_assets() -> QuerySet[Asset]:
    """
    Return all active assets.
    """

    return Asset.objects.all()


def get_organization_assets(
    *,
    organization,
) -> QuerySet[Asset]:
    """
    Return assets belonging to an organization.
    """

    return (
        Asset.objects.all()
        .filter(
            organization=organization,
        )
        .order_by("-created_at")
    )


def get_folder_assets(
    *,
    folder,
) -> QuerySet[Asset]:
    """
    Return assets contained in a folder.
    """

    return (
        Asset.objects.all()
        .filter(
            folder=folder,
        )
        .order_by("-created_at")
    )


def get_assets_by_category(
    *,
    organization,
    category: str,
) -> QuerySet[Asset]:
    """
    Return organization assets filtered by category.
    """

    return (
        Asset.objects.all()
        .filter(
            organization=organization,
            category=category,
        )
        .order_by("-created_at")
    )


def get_assets_by_status(
    *,
    organization,
    status: str,
) -> QuerySet[Asset]:
    """
    Return organization assets filtered by status.
    """

    return (
        Asset.objects.all()
        .filter(
            organization=organization,
            status=status,
        )
        .order_by("-created_at")
    )


def get_assets_by_provider(
    *,
    organization,
    provider: str,
) -> QuerySet[Asset]:
    """
    Return organization assets stored by a provider.
    """

    return (
        Asset.objects.all()
        .filter(
            organization=organization,
            provider=provider,
        )
        .order_by("-created_at")
    )


def search_assets(
    *,
    organization,
    query: str,
) -> QuerySet[Asset]:
    """
    Search assets by name.
    """

    return (
        Asset.objects.all()
        .filter(
            organization=organization,
            original_name__icontains=query,
        )
        .order_by("-created_at")
    )
