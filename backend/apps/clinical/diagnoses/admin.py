from django.contrib import admin

from apps.clinical.diagnoses.models import Diagnosis


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        "diagnosis_code",
        "diagnosis_description",
        "encounter",
        "diagnosis_type",
        "status",
        "is_primary",
        "present_on_admission",
    )
    list_filter = (
        "diagnosis_type",
        "status",
        "is_primary",
        "present_on_admission",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "diagnosis_code",
        "diagnosis_description",
        "encounter__encounter_number",
    )
