"""
API authentication and tenant-boundary tests for clinical transcription.
"""

from __future__ import annotations

from django.test import SimpleTestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.transcription.api.context import require_tenant_organization


class TranscriptionContextTests(SimpleTestCase):
    def test_unauthenticated_request_is_rejected(self):
        request = APIRequestFactory().get("/api/transcription/jobs/")
        request = Request(request)

        with self.assertRaises(Exception):
            require_tenant_organization(request)

    def test_routes_are_declared(self):
        from apps.transcription.api.urls import urlpatterns

        self.assertGreaterEqual(len(urlpatterns), 7)
