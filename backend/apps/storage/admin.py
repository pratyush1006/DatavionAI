"""
Admin configuration for the Storage application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.storage.models import (
    Asset,
    Folder,
)


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Folder.
    """

    list_display = (
        "name",
        "organization",
        "parent",
        "created_at",
    )

    list_filter = ("organization",)

    search_fields = ("name",)

    ordering = ("name",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """
    Admin configuration for Asset.
    """

    list_display = (
        "original_name",
        "organization",
        "category",
        "provider",
        "status",
        "visibility",
        "size",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "organization",
        "category",
        "provider",
        "status",
        "visibility",
    )

    search_fields = (
        "original_name",
        "name",
        "storage_key",
        "checksum",
    )

    readonly_fields = (
        "id",
        "storage_key",
        "path",
        "checksum",
        "provider",
        "size",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "uploaded_by",
        "folder",
    )

    ordering = ("-created_at",)
