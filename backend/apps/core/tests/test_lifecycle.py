"""
Tests for the Core lifecycle utilities.
"""

from __future__ import annotations

from unittest.mock import patch

from django.test import SimpleTestCase

from apps.core.lifecycle import (
    bootstrap_platform,
    shutdown_platform,
    startup_platform,
)


class LifecycleTestCase(SimpleTestCase):
    """
    Test suite for platform lifecycle utilities.
    """

    @patch("apps.core.lifecycle.bootstrap.logger")
    def test_bootstrap_platform(
        self,
        logger,
    ) -> None:
        """
        Test platform bootstrap.
        """

        bootstrap_platform()

        logger.info.assert_called_once()

    @patch("apps.core.lifecycle.startup.application_started.send")
    @patch("apps.core.lifecycle.startup.bootstrap_platform")
    @patch("apps.core.lifecycle.startup.logger")
    def test_startup_platform(
        self,
        logger,
        bootstrap,
        signal,
    ) -> None:
        """
        Test platform startup.
        """

        startup_platform()

        logger.info.assert_called_once()

        bootstrap.assert_called_once()

        signal.assert_called_once_with(
            sender=None,
        )

    @patch("apps.core.lifecycle.shutdown.application_stopping.send")
    @patch("apps.core.lifecycle.shutdown.logger")
    def test_shutdown_platform(
        self,
        logger,
        signal,
    ) -> None:
        """
        Test platform shutdown.
        """

        shutdown_platform()

        logger.info.assert_called_once()

        signal.assert_called_once_with(
            sender=None,
        )
