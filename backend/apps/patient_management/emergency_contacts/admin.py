"""
Admin configuration for the Emergency Contacts module.
"""

from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone

from apps.patient_management.emergency_contacts.models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """
    Django admin configuration for patient emergency contacts.

    Provides tenant-aware operational visibility while keeping
    domain mutation logic outside the admin layer.
    """

    list_display = (
        "emergency_contact_number",
        "full_name",
        "patient",
        "organization",
        "relationship",
        "mobile_number",
        "is_primary",
        "priority_order",
        "status",
        "is_verified",
        "is_active",
        "created_at",
    )

    list_filter = (
        "organization",
        "status",
        "relationship",
        "is_primary",
        "is_verified",
        "is_legal_guardian",
        "has_medical_power_of_attorney",
        "preferred_contact_method",
        "availability",
        "is_active",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "emergency_contact_number",
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "alternate_mobile_number",
        "home_phone",
        "work_phone",
        "email",
        "patient__medical_record_number",
    )

    ordering = (
        "patient",
        "priority_order",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "id",
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

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Emergency Contact",
            {
                "fields": (
                    "organization",
                    "patient",
                    "emergency_contact_number",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "relationship",
                    "date_of_birth",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "mobile_number",
                    "alternate_mobile_number",
                    "home_phone",
                    "work_phone",
                    "email",
                    "preferred_contact_method",
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address_line_1",
                    "address_line_2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                ),
            },
        ),
        (
            "Priority and Availability",
            {
                "fields": (
                    "is_primary",
                    "priority_order",
                    "availability",
                ),
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "verified_at",
                    "verified_by",
                ),
            },
        ),
        (
            "Legal Authority",
            {
                "fields": (
                    "is_legal_guardian",
                    "has_medical_power_of_attorney",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_active",
                    "is_deleted",
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
                ),
            },
        ),
    )

    actions = ("mark_verified",)

    @admin.action(
        description="Mark selected emergency contacts as verified",
    )
    def mark_verified(
        self,
        request: HttpRequest,
        queryset: QuerySet[EmergencyContact],
    ) -> None:
        """
        Mark selected emergency contacts as verified.

        This admin action updates verification metadata consistently
        instead of changing only the verification flag.
        """

        updated = queryset.filter(
            is_verified=False,
        ).update(
            is_verified=True,
            verified_at=timezone.now(),
            verified_by=request.user,
        )

        self.message_user(
            request,
            (
                f"{updated} emergency contact"
                f"{'' if updated == 1 else 's'} marked as verified."
            ),
        )

    def get_queryset(
        self,
        request: HttpRequest,
    ) -> QuerySet[EmergencyContact]:
        """
        Optimize admin list queries for related objects.
        """

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "patient",
            "organization",
            "verified_by",
        )


__all__ = ("EmergencyContactAdmin",)
