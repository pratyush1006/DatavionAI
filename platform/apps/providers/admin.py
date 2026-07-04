"""
Admin configuration for the Providers app.
"""

from django.contrib import admin

from apps.providers.models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Provider.
    """

    list_display = (
        "provider_number",
        "full_name",
        "provider_type",
        "status",
        "is_accepting_patients",
        "organization",
    )

    list_filter = (
        "provider_type",
        "status",
        "is_accepting_patients",
        "organization",
    )

    search_fields = (
        "provider_number",
        "license_number",
        "employee__first_name",
        "employee__last_name",
        "employee__email",
    )

    ordering = ("provider_number",)

    autocomplete_fields = (
        "organization",
        "employee",
    )
