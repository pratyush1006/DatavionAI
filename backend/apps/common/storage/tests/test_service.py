from django.test import SimpleTestCase

from apps.common.storage.service import (
    StorageService,
)


class TestStorageService(
    SimpleTestCase,
):
    def test_service_initialization(self):

        service = StorageService()

        self.assertIsNotNone(
            service,
        )
