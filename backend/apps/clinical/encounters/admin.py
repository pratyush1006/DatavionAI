from django.contrib import admin

from apps.clinical.encounters.models import Encounter


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = (
        "encounter_number",
        "patient",
        "provider",
        "appointment",
        "status",
        "started_at",
        "ended_at",
        "is_billable",
    )
    list_filter = ("status", "is_billable", "is_active", "is_deleted")
    search_fields = ("encounter_number", "patient__mrn", "provider__provider_number")
