"""
Tests for the Core Health API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.constants import (
    ALIVE,
    APP_NAME,
    APP_VERSION,
    HEALTHY,
    READY,
)


class HealthAPITestCase(APITestCase):
    """
    Test suite for Core health endpoints.
    """

    def test_health_endpoint_returns_healthy(self) -> None:
        """
        Test the overall application health endpoint.
        """

        response = self.client.get(
            reverse("core:health:health"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["application"],
            APP_NAME,
        )

        self.assertEqual(
            response.data["version"],
            APP_VERSION,
        )

        self.assertEqual(
            response.data["status"],
            HEALTHY,
        )

        self.assertIn(
            "checks",
            response.data,
        )

        self.assertIn(
            "database",
            response.data["checks"],
        )

    def test_liveness_endpoint_returns_alive(self) -> None:
        """
        Test the liveness endpoint.
        """

        response = self.client.get(
            reverse("core:health:liveness"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            ALIVE,
        )

    def test_readiness_endpoint_returns_ready(self) -> None:
        """
        Test the readiness endpoint.
        """

        response = self.client.get(
            reverse("core:health:readiness"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["application"],
            APP_NAME,
        )

        self.assertEqual(
            response.data["version"],
            APP_VERSION,
        )

        self.assertEqual(
            response.data["status"],
            READY,
        )

        self.assertIn(
            "checks",
            response.data,
        )

        self.assertIn(
            "database",
            response.data["checks"],
        )
