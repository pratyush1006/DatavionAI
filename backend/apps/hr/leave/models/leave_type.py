from django.db import models

from apps.core.models import TimeStampedModel
from apps.platform.organizations.models import Organization


class LeaveType(TimeStampedModel):
    """
    Represents a category of leave an organization offers,
    e.g. Annual Leave, Sick Leave, Maternity Leave.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="leave_types",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=20,
    )

    description = models.TextField(
        blank=True,
    )

    is_paid = models.BooleanField(
        default=True,
    )

    requires_approval = models.BooleanField(
        default=True,
    )

    max_days_per_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    allow_carry_forward = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_leave_type_code_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the leave type display name.
        """

        return f"{self.organization.name} - {self.name}"


__all__ = [
    "LeaveType",
]
