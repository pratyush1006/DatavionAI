"""
Canonical storage client tests.

The legacy storage service has been retired.

This module validates the application-facing StorageClient contract.
"""

from __future__ import annotations

from unittest.mock import Mock

from django.test import SimpleTestCase

from apps.common.storage.client import StorageClient


class StorageClientTests(SimpleTestCase):
    """Tests for the canonical storage client."""

    def setUp(self) -> None:
        self.backend = Mock()

        self.client = StorageClient(
            self.backend,
        )

    def test_upload_delegates_to_backend(self) -> None:
        expected = object()

        self.backend.upload.return_value = expected

        result = self.client.upload(
            "documents/example.pdf",
            b"content",
        )

        self.assertIs(
            result,
            expected,
        )

        self.backend.upload.assert_called_once_with(
            "documents/example.pdf",
            b"content",
            overwrite=False,
        )

    def test_upload_supports_overwrite(self) -> None:
        expected = object()

        self.backend.upload.return_value = expected

        result = self.client.upload(
            "documents/example.pdf",
            b"content",
            overwrite=True,
        )

        self.assertIs(
            result,
            expected,
        )

        self.backend.upload.assert_called_once_with(
            "documents/example.pdf",
            b"content",
            overwrite=True,
        )

    def test_download_delegates_to_backend(self) -> None:
        self.backend.download.return_value = b"content"

        result = self.client.download(
            "documents/example.pdf",
        )

        self.assertEqual(
            result,
            b"content",
        )

        self.backend.download.assert_called_once_with(
            "documents/example.pdf",
        )

    def test_delete_delegates_to_backend(self) -> None:
        self.backend.delete.return_value = True

        result = self.client.delete(
            "documents/example.pdf",
        )

        self.assertTrue(
            result,
        )

        self.backend.delete.assert_called_once_with(
            "documents/example.pdf",
        )

    def test_exists_delegates_to_backend(self) -> None:
        self.backend.exists.return_value = True

        result = self.client.exists(
            "documents/example.pdf",
        )

        self.assertTrue(
            result,
        )

        self.backend.exists.assert_called_once_with(
            "documents/example.pdf",
        )

    def test_url_delegates_to_backend(self) -> None:
        expected = "https://example.invalid/file"

        self.backend.get_url.return_value = expected

        result = self.client.url(
            "documents/example.pdf",
        )

        self.assertEqual(
            result,
            expected,
        )

        self.backend.get_url.assert_called_once_with(
            "documents/example.pdf",
            expires_in=None,
        )

    def test_size_delegates_to_backend(self) -> None:
        self.backend.size.return_value = 123

        result = self.client.size(
            "documents/example.pdf",
        )

        self.assertEqual(
            result,
            123,
        )

        self.backend.size.assert_called_once_with(
            "documents/example.pdf",
        )
