"""
Admin configuration for the Family Members module.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.family_members.models import (
    FamilyMember,
)

__all__ = []


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for FamilyMember.
    """

    list_display = (
        "family_member_number",
        "full_name",
        "patient",
        "relationship",
        "mobile_number",
        "is_next_of_kin",
        "is_emergency_contact",
        "status",
        "is_active",
        "created_at",
    )

    list_filter = (
        "relationship",
        "gender",
        "status",
        "is_living",
        "is_next_of_kin",
        "is_emergency_contact",
        "is_active",
        "created_at",
    )

    search_fields = (
        "family_member_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "email",
        "patient__patient_number",
        "patient__first_name",
        "patient__last_name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

    ordering = (
        "first_name",
        "last_name",
    )

    list_select_related = (
        "organization",
        "patient",
    )

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "family_member_number",
                    "relationship",
                    "status",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "blood_group",
                    "occupation",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "mobile_number",
                    "email",
                    "address",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                ),
            },
        ),
        (
            "Relationship",
            {
                "fields": (
                    "is_living",
                    "is_next_of_kin",
                    "is_emergency_contact",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("notes",),
            },
        ),
        (
            "Audit Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
            },
        ),
    )
