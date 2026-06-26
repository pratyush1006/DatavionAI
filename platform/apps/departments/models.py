from django.db import models

from apps.core.models import TimeStampedModel
from apps.organizations.models import Organization


class Department(TimeStampedModel):
    """
    Represents a department within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=20,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["organization", "code"],
                name="unique_department_code_per_organization",
            ),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.name}"