from __future__ import annotations

from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from apps.imaging.api.views import ImagingContractAPIView
from apps.imaging.services.production_readiness import (
    production_readiness_report,
    run_production_readiness_checks,
)


class ImagingProductionHardeningTests(SimpleTestCase):
    def test_contract_api_requires_authentication_permission(self):
        self.assertIn(
            "ImagingAuthenticatedPermission",
            [cls.__name__ for cls in ImagingContractAPIView.permission_classes],
        )

    @override_settings(
        DEBUG=False,
        SECRET_KEY="production-test-secret",
        ALLOWED_HOSTS=["testserver"],
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
        SECURE_SSL_REDIRECT=True,
        SECURE_HSTS_SECONDS=3600,
        REDIS_URL="redis://localhost:6379/0",
        IMAGING_EVENT_PUBLISHER="tests.publisher",
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}
        },
    )
    @patch(
        "apps.imaging.services.production_readiness._database_ok",
        return_value=(True, "database ok"),
    )
    def test_strict_readiness_can_be_green(self, _database_ok):
        report = production_readiness_report(strict=True)
        self.assertEqual(report["status"], "ready")
        self.assertTrue(all(item["ok"] for item in report["checks"].values()))

    @override_settings(
        DEBUG=True,
        SECRET_KEY="production-test-secret",
        ALLOWED_HOSTS=["testserver"],
        SESSION_COOKIE_SECURE=False,
        CSRF_COOKIE_SECURE=False,
        REDIS_URL="",
        IMAGING_EVENT_PUBLISHER="",
        STORAGES={},
    )
    @patch(
        "apps.imaging.services.production_readiness._database_ok",
        return_value=(True, "database ok"),
    )
    def test_strict_readiness_blocks_missing_production_controls(self, _database_ok):
        checks = run_production_readiness_checks(strict=True)
        failed = {c.name for c in checks if not c.ok and c.severity == "error"}
        self.assertTrue(
            {
                "debug_disabled",
                "secure_session_cookie",
                "secure_csrf_cookie",
                "redis",
                "imaging_event_publisher",
                "storage",
            }.issubset(failed)
        )
