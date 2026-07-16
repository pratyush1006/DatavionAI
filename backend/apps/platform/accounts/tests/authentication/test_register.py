"""
Tests for user registration.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase

User = get_user_model()


class RegisterAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Register API.
    """

    endpoint = "/api/auth/register/"

    def test_register_success(
        self,
    ) -> None:
        """
        A user can register successfully.
        """

        payload = self.register_payload()

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

        user = User.objects.get(
            email=payload["email"],
        )

        self.assertEqual(
            user.first_name,
            payload["first_name"],
        )

        self.assertEqual(
            user.last_name,
            payload["last_name"],
        )

        self.assertTrue(
            user.check_password(
                payload["password"],
            ),
        )

    def test_register_duplicate_email(
        self,
    ) -> None:
        """
        Registration fails when the email already exists.
        """

        self.create_user()

        payload = self.register_payload()

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

    def test_register_invalid_email(
        self,
    ) -> None:
        """
        Registration fails with an invalid email.
        """

        payload = self.register_payload(
            email="invalid-email",
        )

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.count(),
            0,
        )

    def test_register_weak_password(
        self,
    ) -> None:
        """
        Registration fails when the password
        does not satisfy validators.
        """

        payload = self.register_payload(
            password="123",
        )

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.count(),
            0,
        )

    def test_register_missing_required_fields(
        self,
    ) -> None:
        """
        Registration fails when required
        fields are missing.
        """

        response = self.client.post(
            self.endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            User.objects.count(),
            0,
        )

    def test_password_is_hashed(
        self,
    ) -> None:
        """
        Password must never be stored in plain text.
        """

        payload = self.register_payload()

        self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        user = User.objects.get(
            email=payload["email"],
        )

        self.assertNotEqual(
            user.password,
            payload["password"],
        )

        self.assertTrue(
            user.check_password(
                payload["password"],
            ),
        )

    def test_response_does_not_expose_password(
        self,
    ) -> None:
        """
        Password should never appear
        in the response body.
        """

        payload = self.register_payload()

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertNotIn(
            "password",
            response.data,
        )

        self.assertNotIn(
            "password",
            str(response.data),
        )
