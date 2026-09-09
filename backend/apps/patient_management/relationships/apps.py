from __future__ import annotations

from django.apps import AppConfig


class RelationshipsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.relationships"
    label = "patient_relationships"
    verbose_name = "Patient Relationships"

    def ready(self):
        from . import workflow_registry  # noqa: F401
