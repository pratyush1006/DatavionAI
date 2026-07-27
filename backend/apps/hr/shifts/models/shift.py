from django.db import models

from apps.core.models import TimeStampedModel
from apps.platform.organizations.models import Organization


class Shift(TimeStampedModel):
    """
    Represents a reusable work shift template, e.g. Morning,
    Evening, or Night shift.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="shifts",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=20,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    break_minutes = models.PositiveIntegerField(
        default=0,
    )

    is_night_shift = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "start_time",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_shift_code_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the shift display name.
        """

        return f"{self.organization.name} - {self.name}"


__all__ = [
    "Shift",
]
