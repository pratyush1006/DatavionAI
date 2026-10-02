"""Clinical Appointment domain-service tests."""

from __future__ import annotations

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils import timezone

from apps.clinical.appointments.services import AppointmentService


class AppointmentServiceContractTests(SimpleTestCase):
    """Validate core service invariants without requiring fixtures."""

    def test_window_rejects_zero_duration(self):
        """A zero-duration appointment must be rejected."""

        now = timezone.now()

        with self.assertRaises(
            ValidationError,
        ):
            AppointmentService._window(
                scheduled_start=now,
                scheduled_end=now,
                duration_minutes=0,
            )

    def test_window_calculates_duration(self):
        """A valid window returns the calculated duration."""

        start = timezone.now() + timedelta(
            hours=2,
        )
        end = start + timedelta(
            minutes=45,
        )

        normalized_start, normalized_end, duration = AppointmentService._window(
            scheduled_start=start,
            scheduled_end=end,
            duration_minutes=30,
        )

        self.assertEqual(
            normalized_start,
            start,
        )
        self.assertEqual(
            normalized_end,
            end,
        )
        self.assertEqual(
            duration,
            45,
        )


__all__ = ("AppointmentServiceContractTests",)
