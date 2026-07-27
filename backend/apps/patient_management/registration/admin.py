"""
Admin configuration for the Patient Registration module.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.patient_management.registration.models import (
    PatientRegistration,
)


@admin.register(PatientRegistration)
class PatientRegistrationAdmin(admin.ModelAdmin):
    """
    Admin interface for PatientRegistration.
    """

    list_display = (
        "registration_number",
        "patient",
        "organization",
        "registration_type",
        "registration_status",
        "visit_type",
        "priority",
        "verified",
        "registration_datetime",
    )

    list_filter = (
        "registration_status",
        "registration_type",
        "registration_source",
        "visit_type",
        "priority",
        "verified",
        "organization",
    )

    search_fields = (
        "registration_number",
        "patient__first_name",
        "patient__last_name",
        "patient__medical_record_number",
    )

    ordering = ("-registration_datetime",)

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
        "verified_at",
        "checked_in_at",
        "completed_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "verified_by",
    )

    list_select_related = (
        "organization",
        "patient",
        "verified_by",
    )

    date_hierarchy = "registration_datetime"

    list_per_page = 50

    save_on_top = True

    actions = ("mark_verified",)

    fieldsets = (
        (
            _("Registration"),
            {
                "fields": (
                    "organization",
                    "patient",
                    "registration_number",
                    "registration_type",
                    "registration_status",
                    "registration_source",
                    "visit_type",
                    "priority",
                ),
            },
        ),
        (
            _("Verification"),
            {
                "fields": (
                    "verified",
                    "verification_method",
                    "verified_by",
                    "verified_at",
                ),
            },
        ),
        (
            _("Timeline"),
            {
                "fields": (
                    "registration_datetime",
                    "checked_in_at",
                    "completed_at",
                ),
            },
        ),
        (
            _("Cancellation"),
            {
                "fields": (
                    "cancellation_reason",
                    "cancellation_notes",
                ),
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": ("notes",),
            },
        ),
        (
            _("Audit"),
            {
                "classes": ("collapse",),
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.action(
        description=_("Mark selected registrations as verified"),
    )
    def mark_verified(
        self,
        request,
        queryset,
    ) -> None:
        """
        Mark registrations as verified.
        """

        queryset.update(
            verified=True,
        )
