"""
Tests for Laboratory Order API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.clinical.laboratories.constants import LaboratoryPriority
from apps.common.tests.base import BaseAPITestCase


class LaboratoryOrderAPITestCase(
    BaseAPITestCase,
):
    """
    API tests for Laboratory Orders.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

        self.list_url = reverse(
            "laboratories:laboratory_order:list-create",
        )

    ###########################################################################
    # Authentication
    ###########################################################################

    def test_list_orders(
        self,
    ) -> None:
        """
        Authenticated user should list laboratory orders.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Anonymous user should not access the endpoint.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    ###########################################################################
    # Create
    ###########################################################################

    def test_create_laboratory_order(
        self,
    ) -> None:
        """
        Should create a laboratory order.
        """

        patient = self.create_patient()

        provider = self.create_provider()

        encounter = self.create_encounter(
            patient=patient,
            provider=provider,
        )

        payload = {
            "organization": self.organization.id,
            "patient": patient.id,
            "provider": provider.id,
            "encounter": encounter.id,
            "order_number": "LAB999999",
            "priority": LaboratoryPriority.ROUTINE,
            "ordered_at": "2026-07-08T12:00:00Z",
            "clinical_notes": "",
            "instructions": "",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_invalid_payload(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    ###########################################################################
    # Response
    ###########################################################################

    def test_list_response_contains_data(
        self,
    ) -> None:
        """
        Response should contain data.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNotNone(
            response.data,
        )


class LaboratoryTestAPITestCase(
    BaseAPITestCase,
):
    """
    API tests for Laboratory Tests.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.laboratory_order = self.create_laboratory_order()

        self.laboratory_test = self.create_laboratory_test(
            laboratory_order=self.laboratory_order,
        )

        self.list_url = reverse(
            "laboratories:laboratory_test:list-create",
        )

    ###########################################################################
    # Authentication
    ###########################################################################

    def test_list_tests(
        self,
    ) -> None:
        """
        Authenticated user should list laboratory tests.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Anonymous user should not access the endpoint.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    ###########################################################################
    # Create
    ###########################################################################

    def test_create_laboratory_test(
        self,
    ) -> None:
        """
        Should create a laboratory test.
        """

        payload = {
            "laboratory_order": (self.laboratory_order.id),
            "code": "CBC001",
            "name": "Complete Blood Count",
            "category": "hematology",
            "specimen_type": "blood",
            "priority": "routine",
            "notes": "",
            "display_order": 2,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_invalid_payload(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    ###########################################################################
    # Response
    ###########################################################################

    def test_list_response_contains_data(
        self,
    ) -> None:
        """
        Response should contain data.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNotNone(
            response.data,
        )


###############################################################################
# Laboratory Result API
###############################################################################


class LaboratoryResultAPITestCase(
    BaseAPITestCase,
):
    """
    API tests for Laboratory Results.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.result = self.create_laboratory_result()

        self.list_url = reverse(
            "laboratories:laboratory_result:list-create",
        )

    ###########################################################################
    # Authentication
    ###########################################################################

    def test_list_results(
        self,
    ) -> None:
        """
        Authenticated user should list laboratory results.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Anonymous user should not access endpoint.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    ###########################################################################
    # Create
    ###########################################################################

    def test_create_laboratory_result(
        self,
    ) -> None:
        """
        Should create a laboratory result.
        """

        laboratory_test = self.create_laboratory_test()

        payload = {
            "laboratory_test": laboratory_test.id,
            "result_value_numeric": "14.2000",
            "result_value_text": "",
            "unit": "g/dL",
            "reference_range": "12-16",
            "abnormal_flag": "normal",
            "resulted_at": "2026-07-09T10:00:00Z",
            "notes": "",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_invalid_payload(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    ###########################################################################
    # Response
    ###########################################################################

    def test_list_response_contains_data(
        self,
    ) -> None:
        """
        Response should contain data.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNotNone(
            response.data,
        )


__all__ = [
    "LaboratoryOrderAPITestCase",
    "LaboratoryTestAPITestCase",
    "LaboratoryResultAPITestCase",
]
