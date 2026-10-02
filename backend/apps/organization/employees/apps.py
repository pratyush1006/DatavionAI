"""
Employees application configuration.

Employee bounded context.

Responsible for:

- Employee identity
- Employment lifecycle
- Workforce profile
- Employee domain workflows
- Employee domain integrations
"""

from __future__ import annotations

from django.apps import AppConfig


class EmployeesConfig(
    AppConfig,
):
    """
    Employee domain application configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.organization.employees"

    label = "employees"

    verbose_name = "Employees"

    _initialized = False

    def ready(
        self,
    ) -> None:
        """
        Initialize employee domain integrations.

        Registers:

        - Employee workflows
        - Domain events
        - Future signals
        """

        if self._initialized:
            return

        self._initialized = True

        #
        # Register workflows
        #
        from apps.organization.employees.workflow_registry import (
            register_employee_workflows,
        )

        register_employee_workflows()

        #
        # Future:
        #
        # register_employee_events()
        #
        # register_employee_signals()
        #
