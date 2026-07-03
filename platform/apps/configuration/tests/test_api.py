"""
Tests for Configuration API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_GENERAL,
    CONFIGURATION_TYPE_STRING,
)
from apps.configuration.models import (
    Configuration,
)


class ConfigurationAPITestCase(APITestCase):
    """
    Tests for Configuration API endpoints.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="password",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.configuration = Configuration.objects.create(
            key="PLATFORM_NAME",
            category=CONFIGURATION_CATEGORY_GENERAL,
            name="Platform Name",
            description="Platform display name.",
            value="Datavion AI",
            value_type=CONFIGURATION_TYPE_STRING,
            is_editable=True,
        )

    def test_list_configurations(self):
        """
        Should return configuration list.
        """

        response = self.client.get(
            reverse(
                "configuration-api:configuration-list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

        self.assertEqual(
            response.data["meta"]["pagination"]["count"],
            1,
        )

    def test_retrieve_configuration(self):
        """
        Should return configuration details.
        """

        response = self.client.get(
            reverse(
                "configuration-api:configuration-detail",
                kwargs={
                    "key": self.configuration.key,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["key"],
            self.configuration.key,
        )

    def test_create_configuration(self):
        """
        Should create a configuration.
        """

        response = self.client.post(
            reverse(
                "configuration-api:configuration-list-create",
            ),
            {
                "key": "DEFAULT_LANGUAGE",
                "category": CONFIGURATION_CATEGORY_GENERAL,
                "name": "Default Language",
                "description": "Application language.",
                "value": "en",
                "value_type": CONFIGURATION_TYPE_STRING,
                "is_editable": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Configuration.objects.filter(
                key="DEFAULT_LANGUAGE",
            ).exists()
        )

    def test_update_configuration(self):
        """
        Should update a configuration.
        """

        response = self.client.patch(
            reverse(
                "configuration-api:configuration-detail",
                kwargs={
                    "key": self.configuration.key,
                },
            ),
            {
                "value": "Datavion Platform",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.configuration.refresh_from_db()

        self.assertEqual(
            self.configuration.value,
            "Datavion Platform",
        )

    def test_delete_configuration(self):
        """
        Should soft delete a configuration.
        """

        response = self.client.delete(
            reverse(
                "configuration-api:configuration-detail",
                kwargs={
                    "key": self.configuration.key,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.configuration.refresh_from_db()

        self.assertFalse(
            self.configuration.is_active,
        )

    def test_authentication_required(self):
        """
        Anonymous users should not access the API.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "configuration-api:configuration-list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_invalid_configuration_key(self):
        """
        Invalid configuration key should return 400.
        """

        response = self.client.post(
            reverse(
                "configuration-api:configuration-list-create",
            ),
            {
                "key": "invalid key",
                "category": CONFIGURATION_CATEGORY_GENERAL,
                "name": "Invalid",
                "value": "test",
                "value_type": CONFIGURATION_TYPE_STRING,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_empty_patch_returns_400(self):
        """
        Empty PATCH payload should return 400.
        """

        response = self.client.patch(
            reverse(
                "configuration-api:configuration-detail",
                kwargs={
                    "key": self.configuration.key,
                },
            ),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unknown_configuration_returns_404(self):
        """
        Unknown configuration should return 404.
        """

        response = self.client.get(
            reverse(
                "configuration-api:configuration-detail",
                kwargs={
                    "key": "UNKNOWN_CONFIGURATION",
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
