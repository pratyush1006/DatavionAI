"""Architecture tests for Revenue Analytics."""

from __future__ import annotations

from django.test import SimpleTestCase

from ..models import RevenueMetricSnapshot


class RevenueAnalyticsArchitectureTests(SimpleTestCase):
    """Verify non-negotiable Revenue Analytics architecture."""

    def test_snapshot_has_organization_scope(self) -> None:
        """Verify analytics snapshots are organization scoped."""

        field = RevenueMetricSnapshot._meta.get_field("organization")
        self.assertIsNotNone(field.remote_field.model)

    def test_snapshot_has_unique_reporting_period(self) -> None:
        """Verify reporting-period uniqueness is represented in the model."""

        constraint_names = {
            constraint.name for constraint in RevenueMetricSnapshot._meta.constraints
        }
        self.assertIn(
            "unique_rc_metric_snapshot_period",
            constraint_names,
        )

    def test_snapshot_uses_decimal_money(self) -> None:
        """Verify KPI monetary values use DecimalField."""

        field = RevenueMetricSnapshot._meta.get_field("gross_charges")
        self.assertEqual(field.get_internal_type(), "DecimalField")


__all__ = ("RevenueAnalyticsArchitectureTests",)
