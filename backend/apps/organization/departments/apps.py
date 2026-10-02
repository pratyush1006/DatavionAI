from django.apps import AppConfig


class DepartmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.organization.departments"

    label = "departments"

    def ready(
        self,
    ) -> None:
        """
        Register department workflows.
        """

        from apps.organization.departments.workflow_registry import (
            register_department_workflows,
        )

        register_department_workflows()
