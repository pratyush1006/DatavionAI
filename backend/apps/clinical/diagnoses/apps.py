from django.apps import AppConfig


class DiagnosesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clinical.diagnoses"
    label = "diagnoses"
    verbose_name = "Clinical Diagnoses"
