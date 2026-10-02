"""
Admin configuration for Vitals.
"""

from django.contrib import admin

from apps.clinical.vitals.models import Vital


@admin.register(Vital)
class VitalAdmin(admin.ModelAdmin):
    """
    Admin configuration for Vital.
    """

    list_display = (
        "patient",
        "provider",
        "encounter",
        "recorded_at",
        "pulse",
        "systolic_bp",
        "diastolic_bp",
        "temperature",
        "oxygen_saturation",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "temperature_unit",
        "organization",
        "is_active",
    )

    search_fields = (
        "patient__mrn",
        "patient__first_name",
        "patient__last_name",
        "provider__provider_number",
        "encounter__encounter_number",
    )

    ordering = ("-recorded_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
