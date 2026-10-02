from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notes"
    verbose_name = "Clinical Notes"

    def ready(self) -> None:
        from apps.notes.workflow_registry import register_notes_workflows

        register_notes_workflows()
