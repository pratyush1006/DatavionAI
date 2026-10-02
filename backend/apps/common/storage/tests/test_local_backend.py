from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from apps.common.storage.providers.local import (
    LocalStorageBackend,
)


class TestLocalStorageBackend(
    SimpleTestCase,
):
    def test_upload_download_delete(self):

        with TemporaryDirectory() as path:
            storage = LocalStorageBackend(
                path,
            )

            file_path = "test/file.txt"

            result = storage.upload(
                file_path,
                b"hello",
            )

            self.assertEqual(
                result.path,
                file_path,
            )

            self.assertTrue(
                storage.exists(
                    file_path,
                ),
            )

            content = storage.download(
                file_path,
            )

            self.assertEqual(
                content,
                b"hello",
            )

            deleted = storage.delete(
                file_path,
            )

            self.assertTrue(
                deleted,
            )

            self.assertFalse(
                storage.exists(
                    file_path,
                ),
            )
