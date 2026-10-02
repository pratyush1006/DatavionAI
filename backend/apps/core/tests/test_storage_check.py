from django.core.checks import Warning
from django.test import SimpleTestCase, override_settings

from apps.core.checks.storage import storage_check


class StorageCheckRegressionTests(SimpleTestCase):
    @override_settings(
        DEFAULT_FILE_STORAGE="",
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}
        },
    )
    def test_modern_storages_default_backend_satisfies_w002(self):
        messages = storage_check()
        self.assertFalse(
            any(getattr(message, "id", None) == "datavion.W002" for message in messages)
        )

    @override_settings(DEFAULT_FILE_STORAGE="", STORAGES={})
    def test_missing_storage_backend_reports_w002(self):
        messages = storage_check()
        matching = [
            message
            for message in messages
            if getattr(message, "id", None) == "datavion.W002"
        ]
        self.assertEqual(len(matching), 1)
        self.assertIsInstance(matching[0], Warning)
