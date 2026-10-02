from django.contrib import admin

from apps.clinical.medications.models import (
    Medication,
    MedicationAuditLog,
    MedicationOutboxEvent,
)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = (
        "medication_code",
        "generic_name",
        "brand_name",
        "strength",
        "dosage_form",
        "route",
        "is_controlled",
        "is_active",
        "is_deleted",
    )
    list_filter = ("is_active", "is_deleted", "is_controlled", "dosage_form", "route")
    search_fields = ("medication_code", "generic_name", "brand_name", "manufacturer")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")


@admin.register(MedicationAuditLog)
class MedicationAuditLogAdmin(admin.ModelAdmin):
    list_display = ("organization", "medication", "action", "actor_id", "created_at")
    readonly_fields = tuple(field.name for field in MedicationAuditLog._meta.fields)


@admin.register(MedicationOutboxEvent)
class MedicationOutboxEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "aggregate_type",
        "status",
        "attempts",
        "available_at",
        "created_at",
    )
    list_filter = ("status", "event_type")
    readonly_fields = tuple(field.name for field in MedicationOutboxEvent._meta.fields)
