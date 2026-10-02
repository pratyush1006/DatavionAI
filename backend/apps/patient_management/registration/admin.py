"""
Django admin configuration for the Patient Registration module.

The admin interface is intended for inspection and controlled management.
Lifecycle mutations must use the canonical workflow layer rather than
performing direct queryset updates.
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

    The admin is read-oriented with respect to lifecycle state. Lifecycle
    transitions are intentionally not implemented through direct queryset
    updates so that policy, service, audit, and domain-event behavior remain
    consistent across application entry points.
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
        "patient__mrn",
    )

    ordering = ("-registration_datetime",)

    readonly_fields = (
        "uuid",
        "registration_number",
        "registration_status",
        "verified",
        "verification_method",
        "verified_by",
        "verified_at",
        "checked_in_at",
        "completed_at",
        "created_at",
        "updated_at",
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


__all__ = ("PatientRegistrationAdmin",)
