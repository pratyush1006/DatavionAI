"""
Admin configuration for Patient Family Members.
"""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.family_members.models import FamilyMember


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
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
        "family_member_number",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

    list_select_related = (
        "organization",
        "patient",
    )

    ordering = (
        "first_name",
        "last_name",
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


__all__ = ()
