"""
Employee emergency contact model.

Stores emergency contact information for employees.

Responsibilities
----------------
- Emergency contacts
- Relationship information
- Contact details
- Primary emergency contact

Non-responsibilities
--------------------
- Employee identity
- Employee profile
- Addresses
- Employment information
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    RelationshipType,
)


class EmployeeEmergencyContact(
    BaseModel,
):
    """
    Emergency contact for an employee.

    An employee can have multiple emergency contacts,
    but only one primary emergency contact.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this emergency contact.",
        ),
    )

    name = models.CharField(
        _("Full Name"),
        max_length=200,
    )

    relationship = models.CharField(
        _("Relationship"),
        max_length=50,
        choices=RelationshipType.choices,
        help_text=_(
            "Relationship with the employee.",
        ),
    )

    phone_number = models.CharField(
        _("Phone Number"),
        max_length=30,
    )

    alternate_phone_number = models.CharField(
        _("Alternate Phone Number"),
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        _("Email"),
        blank=True,
    )

    is_primary = models.BooleanField(
        _("Primary Contact"),
        default=False,
        help_text=_(
            "Whether this is the employee's primary emergency contact.",
        ),
    )

    notes = models.TextField(
        _("Notes"),
        blank=True,
        help_text=_(
            "Additional emergency contact notes.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_emergency_contacts"

        verbose_name = _(
            "Employee Emergency Contact",
        )

        verbose_name_plural = _(
            "Employee Emergency Contacts",
        )

        ordering = (
            "employee",
            "-is_primary",
            "name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=("employee",),
                condition=models.Q(
                    is_primary=True,
                ),
                name=("uq_employee_primary_emergency_contact"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "employee",
                ],
                name=("idx_emp_emergency_employee"),
            ),
            models.Index(
                fields=[
                    "employee",
                    "is_primary",
                ],
                name=("idx_emp_emergency_primary"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.name}"


__all__: tuple[str, ...] = ("EmployeeEmergencyContact",)
