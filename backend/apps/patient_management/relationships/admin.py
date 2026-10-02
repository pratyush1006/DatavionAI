from django.contrib import admin

from apps.patient_management.relationships.models import PatientRelationship


@admin.register(PatientRelationship)
class PatientRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "organization",
        "patient",
        "related_patient",
        "relationship_type",
        "is_primary",
        "status",
        "verification_status",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "relationship_type",
        "status",
        "verification_status",
        "is_primary",
        "is_active",
        "is_deleted",
    )
    search_fields = ("id", "relationship_name", "notes")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
