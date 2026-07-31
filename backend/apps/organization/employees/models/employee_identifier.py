"""
Employee identifier model.

Stores official identifiers associated with an employee.

Responsibilities
----------------
- Employee IDs
- Professional licenses
- Government identifiers
- Registration numbers
- Identifier verification state

Non-responsibilities
--------------------
- Employment information
- Documents
- Contracts
- Encryption implementation

Encryption and secure storage are handled by
the security infrastructure layer.
"""

from __future__ import annotations

from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    IdentifierType,
    VerificationStatus,
)


class EmployeeIdentifier(
    BaseModel,
):
    """
    Official identifier associated with an employee.

    Sensitive identifier values should be handled through
    security services before persistence.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="identifiers",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee owning this identifier.",
        ),
    )

    identifier_type = models.CharField(
        _("Identifier Type"),
        max_length=30,
        choices=IdentifierType.choices,
        db_index=True,
    )

    identifier_number = models.CharField(
        _("Identifier Number"),
        max_length=150,
        blank=True,
        help_text=_(
            "Encrypted identifier value.",
        ),
    )

    identifier_hash = models.CharField(
        _("Identifier Hash"),
        max_length=255,
        blank=True,
        help_text=_(
            "Secure hash used for identifier lookup.",
        ),
    )

    last_four_digits = models.CharField(
        _("Last Four Digits"),
        max_length=4,
        blank=True,
        help_text=_(
            "Last four characters used for safe display.",
        ),
    )

    issuing_authority = models.CharField(
        _("Issuing Authority"),
        max_length=200,
        blank=True,
    )

    issue_date = models.DateField(
        _("Issue Date"),
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        _("Expiry Date"),
        null=True,
        blank=True,
    )

    verification_status = models.CharField(
        _("Verification Status"),
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    is_primary = models.BooleanField(
        _("Primary Identifier"),
        default=False,
        help_text=_(
            "Whether this is the employee's primary identifier of this type.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_identifiers"

        verbose_name = _(
            "Employee Identifier",
        )

        verbose_name_plural = _(
            "Employee Identifiers",
        )

        ordering = (
            "employee",
            "identifier_type",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "employee",
                    "identifier_type",
                    "identifier_hash",
                ),
                name=("uq_employee_identifier_hash"),
            ),
            models.UniqueConstraint(
                fields=(
                    "employee",
                    "identifier_type",
                ),
                condition=Q(
                    is_primary=True,
                ),
                name=("uq_employee_primary_identifier"),
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        expiry_date__isnull=True,
                    )
                    | Q(
                        issue_date__isnull=True,
                    )
                    | Q(
                        expiry_date__gte=F(
                            "issue_date",
                        ),
                    )
                ),
                name=("ck_employee_identifier_dates"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_identifier_employee"),
            ),
            models.Index(
                fields=("identifier_type",),
                name=("idx_emp_identifier_type"),
            ),
            models.Index(
                fields=("identifier_hash",),
                name=("idx_emp_identifier_hash"),
            ),
            models.Index(
                fields=("verification_status",),
                name=("idx_emp_identifier_status"),
            ),
            models.Index(
                fields=("expiry_date",),
                name=("idx_emp_identifier_expiry"),
            ),
        ]

    @property
    def masked_identifier(
        self,
    ) -> str:
        """
        Return safely masked identifier.

        Example:
            ********4321
        """

        if not self.last_four_digits:
            return "********"

        return f"********{self.last_four_digits}"

    def __str__(
        self,
    ) -> str:
        """
        Return human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.identifier_type}"


__all__: tuple[str, ...] = ("EmployeeIdentifier",)
