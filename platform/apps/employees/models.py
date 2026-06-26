from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.departments.models import Department
from apps.organizations.models import Organization
from apps.teams.models import Team


class Employee(TimeStampedModel):
    """
    Represents an employee within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )

    employee_code = models.CharField(
        max_length=20,
    )

    designation = models.CharField(
        max_length=100,
    )

    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="subordinates",
        null=True,
        blank=True,
    )

    hire_date = models.DateField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "employee_code",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "employee_code",
                ],
                name="unique_employee_code_per_organization",
            ),
        ]

    def __str__(self):
        return f"{self.employee_code} - {self.user.get_full_name()}"
