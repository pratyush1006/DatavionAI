"""
Tests for RequestIDMiddleware.
"""

from __future__ import annotations

import uuid

from django.http import HttpResponse
from django.test import (
    RequestFactory,
    TestCase,
)

from apps.common.middleware import RequestIDMiddleware
from apps.common.request_id import get_request_id


class RequestIDMiddlewareTests(TestCase):
    """
    Tests for RequestIDMiddleware.
    """

    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.middleware = RequestIDMiddleware(
            lambda request: HttpResponse("OK"),
        )

    def test_request_id_is_added_to_response(
        self,
    ) -> None:
        """
        Ensure every response includes a valid request ID.
        """

        request = self.factory.get("/")

        response = self.middleware(request)

        self.assertIn(
            "X-Request-ID",
            response,
        )

        uuid.UUID(response["X-Request-ID"])

    def test_request_has_request_id(
        self,
    ) -> None:
        """
        Ensure the request object receives a request ID.
        """

        request = self.factory.get("/")

        self.middleware(request)

        self.assertTrue(
            hasattr(
                request,
                "request_id",
            ),
        )

    def test_request_id_is_cleared_after_request(
        self,
    ) -> None:
        """
        Ensure thread-local storage is cleared after
        successful request processing.
        """

        request = self.factory.get("/")

        self.middleware(request)

        self.assertIsNone(
            get_request_id(),
        )

    def test_request_id_is_cleared_on_exception(
        self,
    ) -> None:
        """
        Ensure thread-local storage is cleared even if
        request processing raises an exception.
        """

        def failing_view(
            request,
        ) -> HttpResponse:
            raise ValueError("Boom")

        middleware = RequestIDMiddleware(
            failing_view,
        )

        request = self.factory.get("/")

        with self.assertRaises(
            ValueError,
        ):
            middleware(request)

        self.assertIsNone(
            get_request_id(),
        )
