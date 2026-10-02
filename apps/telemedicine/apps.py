from __future__ import annotations
from django.apps import AppConfig

class TelemedicineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.telemedicine"
    verbose_name = "Telemedicine"
    def ready(self) -> None:
        from apps.telemedicine.workflow_registry import register_telemedicine_workflows
        register_telemedicine_workflows()
