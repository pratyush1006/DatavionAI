"""
Employee address model.

Stores normalized employee addresses.

Responsibilities
----------------
- Home address
- Current address
- Permanent address
- Office address

Non-responsibilities
--------------------
- Employee identity
- Emergency contacts
- Organization assignment
- Employment information
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import AddressType


class EmployeeAddress(
    BaseModel,
):
    """
    Employee address.

    An employee may have multiple addresses, each identified
    by an address type.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this address.",
        ),
    )

    address_type = models.CharField(
        _("Address Type"),
        max_length=20,
        choices=AddressType.choices,
        db_index=True,
        help_text=_(
            "Classification of the address.",
        ),
    )

    line_1 = models.CharField(
        _("Address Line 1"),
        max_length=255,
    )

    line_2 = models.CharField(
        _("Address Line 2"),
        max_length=255,
        blank=True,
    )

    landmark = models.CharField(
        _("Landmark"),
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        _("City"),
        max_length=100,
    )

    district = models.CharField(
        _("District"),
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        _("State / Province"),
        max_length=100,
    )

    country = models.CharField(
        _("Country"),
        max_length=100,
    )

    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
    )

    is_primary = models.BooleanField(
        _("Primary Address"),
        default=False,
        help_text=_(
            "Whether this is the employee's primary address.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_addresses"

        verbose_name = _(
            "Employee Address",
        )

        verbose_name_plural = _(
            "Employee Addresses",
        )

        ordering = (
            "employee",
            "-is_primary",
            "address_type",
        )

        constraints = [
            models.UniqueConstraint(
                fields=("employee",),
                condition=models.Q(
                    is_primary=True,
                ),
                name=("uq_employee_primary_address"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "employee",
                ],
                name=("idx_emp_addr_employee"),
            ),
            models.Index(
                fields=[
                    "employee",
                    "address_type",
                ],
                name=("idx_emp_addr_type"),
            ),
            models.Index(
                fields=[
                    "city",
                ],
                name=("idx_emp_addr_city"),
            ),
            models.Index(
                fields=[
                    "state",
                ],
                name=("idx_emp_addr_state"),
            ),
            models.Index(
                fields=[
                    "country",
                ],
                name=("idx_emp_addr_country"),
            ),
            models.Index(
                fields=[
                    "postal_code",
                ],
                name=("idx_emp_addr_postal"),
            ),
        ]

    @property
    def formatted_address(
        self,
    ) -> str:
        """
        Return a formatted single-line address.
        """

        parts = [
            self.line_1,
            self.line_2,
            self.landmark,
            self.city,
            self.district,
            self.state,
            self.country,
            self.postal_code,
        ]

        return ", ".join(part for part in parts if part)

    def __str__(
        self,
    ) -> str:
        """
        Return human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.get_address_type_display()}"


__all__: tuple[str, ...] = ("EmployeeAddress",)
