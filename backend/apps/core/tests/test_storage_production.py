from django.test import SimpleTestCase, override_settings

from apps.common.storage.production import (
    storage_is_ready,
    storage_readiness,
    validate_storage_path,
    validate_upload,
)


class StorageProductionHardeningTests(SimpleTestCase):
    @override_settings(
        DEBUG=False,
        DATAVION_ENVIRONMENT="production",
        STORAGES={
            "default": {
                "BACKEND": "storages.backends.s3.S3Storage",
                "OPTIONS": {"bucket_name": "test"},
            }
        },
    )
    def test_object_storage_is_production_safe(self):
        result = storage_readiness()
        self.assertTrue(result.configured)
        self.assertTrue(result.production_safe)
        self.assertTrue(storage_is_ready())

    @override_settings(
        DEBUG=False,
        DATAVION_ENVIRONMENT="production",
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}
        },
    )
    def test_local_filesystem_is_rejected_in_production(self):
        self.assertFalse(storage_readiness().production_safe)
        self.assertFalse(storage_is_ready())

    def test_path_traversal_is_rejected(self):
        for value in (
            "../secret.txt",
            "/secret.txt",
            r"..\secret.txt",
            r"C:\secret.txt",
        ):
            with self.assertRaises(ValueError):
                validate_storage_path(value)
        self.assertEqual(
            validate_storage_path(r"documents\reports\report.pdf"),
            "documents/reports/report.pdf",
        )

    def test_upload_policy(self):
        with self.assertRaises(ValueError):
            validate_upload("malware.exe", 1024)
        with self.assertRaises(ValueError):
            validate_upload("report.pdf", 26 * 1024 * 1024)
        validate_upload("report.pdf", 1024, content_type="application/pdf")

    @override_settings(STORAGES={}, DEFAULT_FILE_STORAGE="")
    def test_missing_backend_is_not_ready(self):
        self.assertFalse(storage_readiness().configured)
        self.assertFalse(storage_is_ready())
