"""
Employee admin configuration.

Admin responsibilities:

- View employee records
- Search employees
- Monitor lifecycle status
- Trigger workflows

Business mutations should happen through
Employee workflows and services.
"""

from __future__ import annotations

from django.contrib import admin

from apps.organization.employees.models import (
    Employee,
)


@admin.register(Employee)
class EmployeeAdmin(
    admin.ModelAdmin,
):
    """
    Employee administration interface.

    Workflow driven:

    Admin
        |
        v
    Employee Workflow
        |
        v
    Employee State Change
        |
        v
    Audit Event
    """

    list_display = (
        "employee_code",
        "display_name",
        "organization",
        "display_departments",
        "display_teams",
        "designation",
        "is_active",
    )

    list_filter = (
        "organization",
        "designation",
        "is_active",
    )

    search_fields = (
        "employee_code",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    ordering = ("employee_code",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def display_name(
        self,
        obj: Employee,
    ) -> str:
        """
        Employee display name.
        """

        return obj.full_name

    display_name.short_description = "Employee"

    def display_departments(
        self,
        obj: Employee,
    ) -> str:
        """
        Resolve departments through
        department memberships.
        """

        departments = (
            obj.department_memberships.filter(
                is_active=True,
            )
            .select_related(
                "department",
            )
            .values_list(
                "department__name",
                flat=True,
            )
        )

        return (
            ", ".join(
                departments,
            )
            or "-"
        )

    display_departments.short_description = "Departments"

    def display_teams(
        self,
        obj: Employee,
    ) -> str:
        """
        Resolve teams through
        team memberships.
        """

        teams = (
            obj.team_memberships.filter(
                is_active=True,
            )
            .select_related(
                "team",
            )
            .values_list(
                "team__name",
                flat=True,
            )
        )

        return (
            ", ".join(
                teams,
            )
            or "-"
        )

    display_teams.short_description = "Teams"
