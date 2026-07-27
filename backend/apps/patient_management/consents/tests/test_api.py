"""
API tests for the Patient Consents module.
"""

from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


class TestConsentAPI:
    """
    Consent API tests.
    """

    def setup_method(self):
        self.client = APIClient()

    def test_list_endpoint_exists(self):
        url = reverse(
            "consents-api:list",
        )

        response = self.client.get(url)

        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_detail_endpoint_exists(self):
        consent = ConsentFactory()

        url = reverse(
            "consents-api:detail",
            kwargs={
                "id": consent.id,
            },
        )

        response = self.client.get(url)

        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_endpoint_exists(self):
        consent = ConsentFactory()

        url = reverse(
            "consents-api:delete",
            kwargs={
                "id": consent.id,
            },
        )

        response = self.client.delete(url)

        assert response.status_code in (
            status.HTTP_204_NO_CONTENT,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
