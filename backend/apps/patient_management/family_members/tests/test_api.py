"""
API tests for the Family Members module.
"""

from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


class TestFamilyMemberAPI:
    """
    Family Member API tests.
    """

    def setup_method(self):
        self.client = APIClient()

    def test_list_endpoint_exists(self):
        url = reverse(
            "family-members-api:list",
        )

        response = self.client.get(url)

        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_detail_endpoint_exists(self):
        member = FamilyMemberFactory()

        url = reverse(
            "family-members-api:detail",
            kwargs={
                "id": member.id,
            },
        )

        response = self.client.get(url)

        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_endpoint_exists(self):
        member = FamilyMemberFactory()

        url = reverse(
            "family-members-api:delete",
            kwargs={
                "id": member.id,
            },
        )

        response = self.client.delete(url)

        assert response.status_code in (
            status.HTTP_204_NO_CONTENT,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
