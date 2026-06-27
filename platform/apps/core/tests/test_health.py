from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckAPITest(APITestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("core:health"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["status"],
            "healthy",
        )

        self.assertEqual(
            response.data["data"]["version"],
            settings.APP_VERSION,
        )

        self.assertIn(
            "database",
            response.data["data"]["checks"],
        )
