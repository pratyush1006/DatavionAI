"""
Tests for platform system checks.
"""

from __future__ import annotations

from django.core.checks import run_checks
from django.test import SimpleTestCase


class CoreSystemChecksTestCase(SimpleTestCase):
    """
    Test execution of the Datavion platform system checks.
    """

    def test_system_checks_execute(self) -> None:
        """
        Ensure custom system checks execute without raising exceptions.
        """

        messages = run_checks()

        self.assertIsInstance(
            messages,
            list,
        )

    def test_database_checks_execute(self) -> None:
        """
        Execute database-tagged checks.
        """

        messages = run_checks(
            tags=["database"],
        )

        self.assertIsInstance(
            messages,
            list,
        )

    def test_cache_checks_execute(self) -> None:
        """
        Execute cache-tagged checks.
        """

        messages = run_checks(
            tags=["caches"],
        )

        self.assertIsInstance(
            messages,
            list,
        )

    def test_security_checks_execute(self) -> None:
        """
        Execute security-tagged checks.
        """

        messages = run_checks(
            tags=["security"],
        )

        self.assertIsInstance(
            messages,
            list,
        )

    def test_file_checks_execute(self) -> None:
        """
        Execute file/storage-tagged checks.
        """

        messages = run_checks(
            tags=["files"],
        )

        self.assertIsInstance(
            messages,
            list,
        )
