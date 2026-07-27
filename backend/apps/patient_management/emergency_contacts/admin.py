"""
Admin configuration for the Emergency Contacts module.
"""

from __future__ import annotations

from django.contrib import admin

from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(
    admin.ModelAdmin,
):
    """
    Emergency contact admin.
    """

    list_display = (
        "emergency_contact_number",
        "full_name",
        "patient",
        "relationship",
        "mobile_number",
        "is_primary",
        "status",
        "is_verified",
    )

    list_filter = (
        "status",
        "relationship",
        "is_primary",
        "is_verified",
        "preferred_contact_method",
    )

    search_fields = (
        "emergency_contact_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "email",
        "patient__medical_record_number",
    )

    ordering = (
        "patient",
        "priority_order",
    )

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
        "verified_at",
    )

    autocomplete_fields = (
        "patient",
        "organization",
        "verified_by",
    )

    list_select_related = (
        "patient",
        "organization",
        "verified_by",
    )

    actions = ("mark_verified",)

    @admin.action(
        description="Mark selected emergency contacts as verified",
    )
    def mark_verified(
        self,
        request,
        queryset,
    ):
        queryset.update(
            is_verified=True,
        )
