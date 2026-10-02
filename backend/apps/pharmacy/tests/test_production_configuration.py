from django.test import SimpleTestCase, override_settings

from apps.pharmacy.services.production_readiness import production_readiness_report


class PharmacyProductionConfigurationTests(SimpleTestCase):
    @override_settings(
        DEBUG=False,
        SECRET_KEY="production-secret",
        ALLOWED_HOSTS=["pharmacy.example.com"],
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}
        },
        REDIS_URL="redis://localhost:6379/0",
        PHARMACY_EVENT_PUBLISHER="apps.pharmacy.tests.factories.publish_event",
    )
    def test_production_configuration_can_be_ready(self):
        report = production_readiness_report()
        self.assertEqual(report["status"], "ready")
        self.assertTrue(all(item["ok"] for item in report["checks"].values()))

    @override_settings(
        DEBUG=True,
        SECRET_KEY="production-secret",
        ALLOWED_HOSTS=["pharmacy.example.com"],
        SESSION_COOKIE_SECURE=False,
        CSRF_COOKIE_SECURE=False,
        REDIS_URL="",
        PHARMACY_EVENT_PUBLISHER="",
        STORAGES={},
    )
    def test_development_configuration_is_not_production_ready(self):
        report = production_readiness_report()
        self.assertEqual(report["status"], "not_ready")
        self.assertFalse(report["checks"]["debug_disabled"]["ok"])
        self.assertFalse(report["checks"]["redis"]["ok"])
        self.assertFalse(report["checks"]["pharmacy_event_publisher"]["ok"])
