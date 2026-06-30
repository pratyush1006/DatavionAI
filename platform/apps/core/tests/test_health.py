from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckAPITest(APITestCase):
    """
    Tests for the application health endpoint.
    """

    def test_health_endpoint(self):
        """
        The health endpoint should return a successful
        application health response.
        """

        response = self.client.get(reverse("core:health"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["status"],
            "healthy",
        )

        self.assertEqual(
            response.data["data"]["version"],
            settings.APP_VERSION,
        )

        self.assertEqual(
            response.data["data"]["checks"]["database"],
            "ok",
        )

        self.assertIn(
            "timestamp",
            response.data["data"],
        )
