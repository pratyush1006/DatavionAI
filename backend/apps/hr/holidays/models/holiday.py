from django.db import models

from apps.core.models import TimeStampedModel
from apps.hr.holidays.constants import (
    DEFAULT_HOLIDAY_TYPE,
    HolidayType,
)
from apps.platform.organizations.models import Organization


class Holiday(TimeStampedModel):
    """
    Represents a single day on an organization's holiday
    calendar, e.g. a public or company holiday.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="holidays",
    )

    name = models.CharField(
        max_length=150,
    )

    date = models.DateField()

    holiday_type = models.CharField(
        max_length=20,
        choices=HolidayType.choices,
        default=DEFAULT_HOLIDAY_TYPE,
    )

    description = models.TextField(
        blank=True,
    )

    is_recurring_yearly = models.BooleanField(
        default=False,
        help_text="Whether this holiday recurs on the same date every year.",
    )

    class Meta:
        ordering = [
            "date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "date",
                    "name",
                ],
                name="unique_holiday_per_organization_per_date",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the holiday display name.
        """

        return f"{self.organization.name} - {self.name} ({self.date})"


__all__ = [
    "Holiday",
]
