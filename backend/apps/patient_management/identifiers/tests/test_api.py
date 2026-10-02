"""
Tests for Patient Identifier API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.common.tests import AuthenticatedAPITestCase
from apps.patient_management.identifiers.tests.factories import (
    PatientIdentifierFactory,
)


class PatientIdentifierAPITestCase(
    AuthenticatedAPITestCase,
):
    """Tests for Patient Identifier API."""

    def test_list_patient_identifiers(self) -> None:
        PatientIdentifierFactory()

        response = self.client.get(
            reverse(
                "patient-identifiers:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
