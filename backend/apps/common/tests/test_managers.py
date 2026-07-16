"""
Tests for reusable model managers.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from django.test import SimpleTestCase

from apps.core.models import BaseManager


class BaseManagerTests(SimpleTestCase):
    """
    Tests for BaseManager.
    """

    def setUp(self) -> None:
        self.manager = BaseManager()

    def test_active_delegates_to_queryset(
        self,
    ) -> None:
        queryset = MagicMock()

        self.manager.get_queryset = MagicMock(
            return_value=queryset,
        )

        self.manager.active()

        queryset.active.assert_called_once_with()

    def test_inactive_delegates_to_queryset(
        self,
    ) -> None:
        queryset = MagicMock()

        self.manager.get_queryset = MagicMock(
            return_value=queryset,
        )

        self.manager.inactive()

        queryset.inactive.assert_called_once_with()

    def test_newest_delegates_to_queryset(
        self,
    ) -> None:
        queryset = MagicMock()

        self.manager.get_queryset = MagicMock(
            return_value=queryset,
        )

        self.manager.newest()

        queryset.newest.assert_called_once_with()
