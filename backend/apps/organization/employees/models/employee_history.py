"""
Employee history model.

Stores immutable employee business lifecycle events.

Responsibilities
----------------
- Employment lifecycle history
- Position changes
- Department transfers
- Manager changes
- Status changes
- Business event timeline

Non-responsibilities
--------------------
- System audit logging
- Workflow execution
- Notifications
- Event publishing

Notes
-----
This model records business history only.

System-level auditing is handled by the Audit module.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    EmployeeHistoryEvent,
)


class EmployeeHistory(
    BaseModel,
):
    """
    Immutable business history for an employee.

    Records meaningful employee lifecycle events.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee associated with this history record.",
        ),
    )

    event_type = models.CharField(
        _("Event Type"),
        max_length=50,
        choices=EmployeeHistoryEvent.choices,
        db_index=True,
        help_text=_(
            "Business event classification.",
        ),
    )

    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_(
            "Short event title.",
        ),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_(
            "Detailed business event description.",
        ),
    )

    effective_date = models.DateField(
        _("Effective Date"),
        help_text=_(
            "Date on which the event became effective.",
        ),
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_history_events",
        verbose_name=_(
            "Performed By",
        ),
        help_text=_(
            "User responsible for the business action.",
        ),
    )

    reference_type = models.CharField(
        _("Reference Type"),
        max_length=100,
        blank=True,
        help_text=_(
            "Optional referenced domain object type.",
        ),
    )

    reference_id = models.UUIDField(
        _("Reference ID"),
        null=True,
        blank=True,
        help_text=_(
            "Optional referenced domain object identifier.",
        ),
    )

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
        help_text=_(
            "Additional business context data.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_history"

        verbose_name = _(
            "Employee History",
        )

        verbose_name_plural = _(
            "Employee History",
        )

        ordering = (
            "-effective_date",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_history_employee"),
            ),
            models.Index(
                fields=(
                    "employee",
                    "event_type",
                ),
                name=("idx_emp_history_employee_event"),
            ),
            models.Index(
                fields=("event_type",),
                name=("idx_emp_history_event"),
            ),
            models.Index(
                fields=("effective_date",),
                name=("idx_emp_history_effective"),
            ),
            models.Index(
                fields=("performed_by",),
                name=("idx_emp_history_user"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.title}"


__all__: tuple[str, ...] = ("EmployeeHistory",)
