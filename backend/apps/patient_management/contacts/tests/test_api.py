"""
Tests for the Contact API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.common.tests import AuthenticatedAPITestCase
from apps.patient_management.contacts.tests.factories import (
    ContactFactory,
)


class ContactAPITestCase(
    AuthenticatedAPITestCase,
):
    """Tests for the Contact API."""

    def test_list_contacts(self) -> None:
        ContactFactory()

        response = self.client.get(
            reverse(
                "patient-contacts:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
