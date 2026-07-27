"""
Manager and QuerySet tests for Emergency Contacts.
"""

from __future__ import annotations

from django.test import TestCase

from .factories import (
    EmergencyContactFactory,
)


class EmergencyContactManagerTestCase(
    TestCase,
):
    """
    Tests for EmergencyContact managers and querysets.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test data.
        """

        self.primary_contact = EmergencyContactFactory(
            first_name="John",
            is_primary=True,
            is_verified=True,
        )

        self.secondary_contact = EmergencyContactFactory(
            first_name="Jane",
            is_primary=False,
            is_verified=False,
            priority_order=2,
        )

    def test_active_manager(self) -> None:
        """
        Active manager returns active contacts.
        """

        queryset = self.primary_contact.__class__.objects.active()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_verified_queryset(self) -> None:
        """
        Verified queryset returns only verified contacts.
        """

        queryset = self.primary_contact.__class__.objects.verified()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.primary_contact,
        )

    def test_unverified_queryset(self) -> None:
        """
        Unverified queryset returns only unverified contacts.
        """

        queryset = self.primary_contact.__class__.objects.unverified()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.secondary_contact,
        )

    def test_primary_queryset(self) -> None:
        """
        Primary queryset returns only primary contacts.
        """

        queryset = self.primary_contact.__class__.objects.primary()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.primary_contact,
        )

    def test_search_queryset(self) -> None:
        """
        Search returns matching contacts.
        """

        queryset = self.primary_contact.__class__.objects.search(
            "John",
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_soft_deleted_not_returned(self) -> None:
        """
        Soft deleted records are excluded
        from the default manager.
        """

        self.secondary_contact.delete()

        queryset = self.primary_contact.__class__.objects.all()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_deleted_manager(self) -> None:
        """
        Deleted manager returns only deleted records.
        """

        self.secondary_contact.delete()

        queryset = self.secondary_contact.__class__.deleted_objects.all()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.secondary_contact,
        )

    def test_all_objects_manager(self) -> None:
        """
        All objects manager returns every record.
        """

        self.secondary_contact.delete()

        queryset = self.secondary_contact.__class__.all_objects.all()

        self.assertEqual(
            queryset.count(),
            2,
        )
