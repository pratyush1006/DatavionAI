"""
Tests for reusable querysets.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from django.test import SimpleTestCase

from apps.core.models import BaseQuerySet


class BaseQuerySetTests(SimpleTestCase):
    """
    Tests for BaseQuerySet.
    """

    def setUp(self) -> None:
        self.queryset = BaseQuerySet(
            model=MagicMock(),
        )

    def test_active_filters_active_records(
        self,
    ) -> None:
        """
        Ensure active() filters active records.
        """

        self.queryset.filter = MagicMock()

        self.queryset.active()

        self.queryset.filter.assert_called_once_with(
            is_active=True,
        )

    def test_inactive_filters_inactive_records(
        self,
    ) -> None:
        """
        Ensure inactive() filters inactive records.
        """

        self.queryset.filter = MagicMock()

        self.queryset.inactive()

        self.queryset.filter.assert_called_once_with(
            is_active=False,
        )

    def test_newest_orders_by_created_at_descending(
        self,
    ) -> None:
        """
        Ensure newest() sorts by newest records first.
        """

        self.queryset.order_by = MagicMock()

        self.queryset.newest()

        self.queryset.order_by.assert_called_once_with(
            "-created_at",
        )
