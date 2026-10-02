"""
Provider availability model.

Defines provider working schedules
for clinical operations.

Supports:

- Appointment scheduling
- Calendar integration
- Provider discovery
- Telemedicine availability
"""

from __future__ import annotations

from django.db import models

from apps.clinical.providers.constants import (
    AvailabilityDay,
    AvailabilityStatus,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class ProviderAvailability(
    BaseModel,
):
    """
    Provider working availability slot.
    """

    objects = BaseManager()

    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.CASCADE,
        related_name="availability",
        help_text=("Provider associated with availability."),
    )

    day_of_week = models.PositiveSmallIntegerField(
        choices=AvailabilityDay.choices,
        help_text=("ISO weekday number."),
    )

    start_time = models.TimeField(
        help_text=("Availability start time."),
    )

    end_time = models.TimeField(
        help_text=("Availability end time."),
    )

    location = models.CharField(
        max_length=150,
        blank=True,
        help_text=("Clinic location or facility."),
    )

    status = models.CharField(
        max_length=30,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE,
        db_index=True,
        help_text=("Availability status."),
    )

    is_recurring = models.BooleanField(
        default=True,
        help_text=("Whether this availability repeats weekly."),
    )

    notes = models.TextField(
        blank=True,
        help_text=("Additional scheduling notes."),
    )

    class Meta:
        db_table = "provider_availability"

        verbose_name = "Provider Availability"

        verbose_name_plural = "Provider Availability"

        ordering = (
            "day_of_week",
            "start_time",
        )

        indexes = [
            models.Index(
                fields=[
                    "provider",
                    "day_of_week",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
        ]

    @property
    def is_available(
        self,
    ) -> bool:
        """
        Check active availability.
        """

        return self.status == AvailabilityStatus.AVAILABLE

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.provider.display_name} - "
            f"{self.get_day_of_week_display()} "
            f"{self.start_time}-{self.end_time}"
        )


__all__ = [
    "ProviderAvailability",
]
