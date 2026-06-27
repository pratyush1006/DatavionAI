from django.test import TestCase
from rest_framework import status

from apps.common.api.responses import (
    created_response,
    no_content_response,
    success_response,
)


class ResponseHelperTest(TestCase):
    def test_success_response(self):
        response = success_response(
            data={"id": 1},
            message="Success",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(response.data["data"]["id"], 1)

    def test_created_response(self):
        response = created_response(
            data={"id": 1},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(response.data["success"])

    def test_no_content_response(self):
        response = no_content_response()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
