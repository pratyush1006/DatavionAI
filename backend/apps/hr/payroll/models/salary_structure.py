from django.db import models

from apps.core.models import TimeStampedModel
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class SalaryStructure(TimeStampedModel):
    """
    Represents an employee's salary structure for a given
    effective period. A new row is created whenever an
    employee's compensation changes, preserving salary history.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="salary_structures",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_structures",
    )

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    house_rent_allowance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    other_allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=3,
        default="USD",
    )

    effective_from = models.DateField()

    effective_to = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "-effective_from",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "effective_from",
                ],
                name="unique_salary_structure_per_employee_per_start_date",
            ),
        ]

    @property
    def gross_salary(
        self,
    ):
        """
        Return the total gross monthly salary.
        """

        return self.basic_salary + self.house_rent_allowance + self.other_allowances

    def __str__(
        self,
    ) -> str:
        """
        Return the salary structure display name.
        """

        return f"{self.employee.employee_code} - {self.effective_from}"


__all__ = [
    "SalaryStructure",
]
