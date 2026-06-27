import uuid

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from apps.common.middleware import RequestIDMiddleware


class RequestIDMiddlewareTests(TestCase):
    def test_request_id_is_added_to_response(self):
        factory = RequestFactory()

        request = factory.get("/")

        middleware = RequestIDMiddleware(lambda request: HttpResponse("OK"))

        response = middleware(request)

        self.assertIn("X-Request-ID", response)

        uuid.UUID(response["X-Request-ID"])
