"""
Admin configuration for the Laboratories application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.laboratories.models import (
    LaboratoryOrder,
    LaboratoryResult,
    LaboratoryTest,
)


@admin.register(LaboratoryOrder)
class LaboratoryOrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for LaboratoryOrder.
    """

    list_display = (
        "order_number",
        "patient",
        "provider",
        "priority",
        "status",
        "ordered_at",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "organization",
        "ordered_at",
    )

    search_fields = (
        "order_number",
        "patient__first_name",
        "patient__last_name",
        "patient__email",
        "provider__employee__first_name",
        "provider__employee__last_name",
        "provider__provider_number",
    )

    ordering = ("-ordered_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "provider",
        "encounter",
    )

    list_select_related = (
        "organization",
        "patient",
        "provider",
        "encounter",
    )

    date_hierarchy = "ordered_at"


@admin.register(LaboratoryTest)
class LaboratoryTestAdmin(admin.ModelAdmin):
    """
    Admin configuration for LaboratoryTest.
    """

    list_display = (
        "name",
        "code",
        "laboratory_order",
        "category",
        "specimen_type",
        "priority",
        "status",
    )

    list_filter = (
        "category",
        "specimen_type",
        "priority",
        "status",
    )

    search_fields = (
        "name",
        "code",
        "laboratory_order__order_number",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("laboratory_order",)

    list_select_related = ("laboratory_order",)


@admin.register(LaboratoryResult)
class LaboratoryResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for LaboratoryResult.
    """

    list_display = (
        "laboratory_test",
        "status",
        "abnormal_flag",
        "verified_by",
        "resulted_at",
    )

    list_filter = (
        "status",
        "abnormal_flag",
        "resulted_at",
    )

    search_fields = (
        "laboratory_test__name",
        "laboratory_test__code",
        "laboratory_test__laboratory_order__order_number",
    )

    ordering = ("-resulted_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "laboratory_test",
        "verified_by",
    )

    list_select_related = (
        "laboratory_test",
        "verified_by",
    )

    date_hierarchy = "resulted_at"


__all__ = [
    "LaboratoryOrderAdmin",
    "LaboratoryResultAdmin",
    "LaboratoryTestAdmin",
]
