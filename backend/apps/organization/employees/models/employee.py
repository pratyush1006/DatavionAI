"""
Employee aggregate root.

Represents the primary employee identity within an organization.

Responsibilities
----------------
- Employee identity
- Organization membership
- Employment lifecycle
- Reporting hierarchy

Non-responsibilities
--------------------
- Department assignments
- Team assignments
- Contracts
- Payroll
- Attendance
- Leave management
- Documents
- Skills
- Emergency contacts
- Employment history

These responsibilities belong to dedicated bounded contexts.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    DEFAULT_EMPLOYMENT_STATUS,
    DEFAULT_EMPLOYMENT_TYPE,
    EmploymentStatus,
    EmploymentType,
)


class Employee(
    BaseModel,
):
    """
    Employee aggregate root.

    Stores the master employee record for an organization.

    All employee-related domain entities reference this model.
    """

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="employees",
        db_index=True,
        verbose_name=_("Organization"),
        help_text=_(
            "Organization that owns this employee.",
        ),
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
        verbose_name=_("User"),
        help_text=_(
            "Linked authentication account.",
        ),
    )

    employee_code = models.CharField(
        _("Employee Code"),
        max_length=50,
        help_text=_(
            "Unique employee identifier within the organization.",
        ),
    )

    designation = models.CharField(
        _("Designation"),
        max_length=150,
        help_text=_(
            "Current employee designation.",
        ),
    )

    # ------------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------------

    work_email = models.EmailField(
        _("Work Email"),
        blank=True,
        db_index=True,
        help_text=_(
            "Official organization email address.",
        ),
    )

    phone_number = models.CharField(
        _("Phone Number"),
        max_length=30,
        blank=True,
        help_text=_(
            "Primary work contact number.",
        ),
    )

    # ------------------------------------------------------------------
    # Employment
    # ------------------------------------------------------------------

    employment_type = models.CharField(
        _("Employment Type"),
        max_length=30,
        choices=EmploymentType.choices,
        default=DEFAULT_EMPLOYMENT_TYPE,
        db_index=True,
    )

    status = models.CharField(
        _("Employment Status"),
        max_length=30,
        choices=EmploymentStatus.choices,
        default=DEFAULT_EMPLOYMENT_STATUS,
        db_index=True,
    )

    joining_date = models.DateField(
        _("Joining Date"),
        help_text=_(
            "Date the employee joined the organization.",
        ),
    )

    confirmation_date = models.DateField(
        _("Confirmation Date"),
        null=True,
        blank=True,
        help_text=_(
            "Date employee completed probation.",
        ),
    )

    termination_date = models.DateField(
        _("Termination Date"),
        null=True,
        blank=True,
        help_text=_(
            "Employment end date.",
        ),
    )

    # ------------------------------------------------------------------
    # Reporting Hierarchy
    # ------------------------------------------------------------------

    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
        verbose_name=_("Manager"),
        help_text=_(
            "Direct reporting manager.",
        ),
    )

    # ------------------------------------------------------------------
    # Extension
    # ------------------------------------------------------------------

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
        help_text=_(
            "Additional non-business metadata.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employees"

        verbose_name = _("Employee")

        verbose_name_plural = _("Employees")

        ordering = ("employee_code",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "employee_code",
                ),
                name="uq_employee_org_code",
            ),
            models.CheckConstraint(
                condition=(
                    Q(
                        termination_date__isnull=True,
                    )
                    | Q(
                        termination_date__gte=F(
                            "joining_date",
                        ),
                    )
                ),
                name="ck_employee_termination_date",
            ),
            models.CheckConstraint(
                condition=~Q(
                    id=F(
                        "manager_id",
                    ),
                ),
                name="ck_employee_not_self_manager",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                ],
                name="idx_employee_org",
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="idx_employee_org_status",
            ),
            models.Index(
                fields=[
                    "organization",
                    "employment_type",
                ],
                name="idx_employee_org_type",
            ),
            models.Index(
                fields=[
                    "manager",
                ],
                name="idx_employee_manager",
            ),
            models.Index(
                fields=[
                    "joining_date",
                ],
                name="idx_employee_joining",
            ),
            models.Index(
                fields=[
                    "termination_date",
                ],
                name="idx_employee_termination",
            ),
            models.Index(
                fields=[
                    "work_email",
                ],
                name="idx_employee_work_email",
            ),
        ]

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return employee display name.

        Falls back to employee code when no linked
        user name exists.
        """

        if self.user is not None:
            name = self.user.get_full_name().strip()

            if name:
                return name

        return self.employee_code

    @property
    def is_active_employee(
        self,
    ) -> bool:
        """
        Return whether employee is actively employed.
        """

        return self.status == EmploymentStatus.ACTIVE

    @property
    def is_terminated(
        self,
    ) -> bool:
        """
        Return whether employee is terminated.
        """

        return self.status == EmploymentStatus.TERMINATED

    def __str__(
        self,
    ) -> str:
        """
        Return human-readable representation.
        """

        return f"{self.employee_code} - {self.full_name}"


__all__: tuple[str, ...] = ("Employee",)
