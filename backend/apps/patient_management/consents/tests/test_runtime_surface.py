from __future__ import annotations

from django.test import SimpleTestCase
from django.urls import Resolver404, resolve


class ConsentsRuntimeSurfaceTests(SimpleTestCase):
    """Minimal runtime safety coverage for the consents API surface."""

    def test_api_surface_resolves(self) -> None:
        path = "/api/patient-management/consents/"

        try:
            match = resolve(path)
        except Resolver404 as exc:
            self.fail(f"Expected {path} to resolve, got: {exc!r}")

        self.assertIsNotNone(match.func)
