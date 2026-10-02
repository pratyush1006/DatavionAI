from django.apps import AppConfig


class EncountersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clinical.encounters"
    label = "encounters"
    verbose_name = "Clinical Encounters"
