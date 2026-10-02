from pathlib import Path
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.documents.services import media


class _FakeStorage:
    def __init__(self):
        self.objects = {}

    def upload(self, path, content, overwrite=False):
        if path in self.objects and not overwrite:
            raise FileExistsError(path)
        self.objects[path] = bytes(content)

    def download(self, path):
        return self.objects[path]

    def delete(self, path):
        return self.objects.pop(path, None) is not None

    def exists(self, path):
        return path in self.objects

    def url(self, path, expires_in=None):
        return f"memory://{path}"

    def size(self, path):
        return len(self.objects[path])


class DocumentsProductionE2ETests(SimpleTestCase):
    def setUp(self):
        self.fake = _FakeStorage()
        self.original = media.get_storage_client
        media.get_storage_client = lambda: self.fake

    def tearDown(self):
        media.get_storage_client = self.original

    def test_declared_media_families(self):
        expected = {"pdf", "image", "office", "audio", "video"}
        self.assertEqual(set(media.MEDIA_TYPES), expected)
        self.assertEqual(set(media.EXTENSIONS), expected)

    def test_mime_extension_mismatch_rejected(self):
        with self.assertRaises(ValidationError):
            media.media_family(filename="voice.mp3", mime_type="video/mp4")
        with self.assertRaises(ValidationError):
            media.media_family(filename="report.pdf", mime_type="image/png")

    def test_unsafe_filename_and_empty_content_rejected(self):
        for name in ("", "../x.pdf", "dir/x.pdf", "dir\\x.pdf", "x\\x00.pdf"):
            with self.assertRaises(ValidationError):
                media.validate_media(filename=name, size=1, mime_type="application/pdf")
        with self.assertRaises(ValidationError):
            media.validate_media(filename="x.pdf", size=0, mime_type="application/pdf")

    def test_sha256_checksum(self):
        payload = b"DatavionOS Documents"
        import hashlib

        self.assertEqual(
            media.checksum_bytes(payload), hashlib.sha256(payload).hexdigest()
        )

    def test_storage_key_is_scoped_and_versioned(self):
        doc = uuid4()
        self.assertEqual(
            media.build_storage_key(
                tenant_id="t",
                organization_id="o",
                document_id=doc,
                filename="a.mp4",
                version_number=3,
            ),
            f"documents/t/o/{doc}/v3.mp4",
        )
        with self.assertRaises(ValidationError):
            media.build_storage_key(
                tenant_id="t",
                organization_id="o",
                document_id=doc,
                filename="a.pdf",
                version_number=0,
            )

    def _roundtrip(self, filename, mime, payload):
        d = media.upload_media(
            content=payload,
            filename=filename,
            mime_type=mime,
            tenant_id="t",
            organization_id="o",
            document_id=uuid4(),
            version_number=1,
        )
        self.assertEqual(d.file_size, len(payload))
        self.assertEqual(d.checksum, media.checksum_bytes(payload))
        self.assertEqual(self.fake.download(d.storage_key), payload)
        self.assertTrue(media.media_exists(storage_key=d.storage_key))
        self.assertEqual(
            media.media_url(storage_key=d.storage_key), f"memory://{d.storage_key}"
        )
        self.assertTrue(media.delete_uploaded_media(storage_key=d.storage_key))
        self.assertFalse(media.media_exists(storage_key=d.storage_key))

    def test_pdf_roundtrip(self):
        self._roundtrip("x.pdf", "application/pdf", b"pdf")

    def test_image_roundtrip(self):
        self._roundtrip("x.png", "image/png", b"png")

    def test_office_roundtrip(self):
        self._roundtrip(
            "x.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            b"docx",
        )

    def test_audio_roundtrip(self):
        self._roundtrip("x.mp3", "audio/mpeg", b"audio")

    def test_video_roundtrip(self):
        self._roundtrip("x.mp4", "video/mp4", b"video")

    def test_document_model_contract(self):
        from apps.documents.models import Document

        fields = {f.name for f in Document._meta.fields}
        self.assertTrue(
            {
                "tenant",
                "organization",
                "storage_key",
                "original_filename",
                "mime_type",
                "file_size",
                "checksum",
                "metadata",
                "ai_metadata",
            }.issubset(fields)
        )

    def test_document_version_contract(self):
        from apps.documents.models import DocumentVersion

        fields = {f.name for f in DocumentVersion._meta.fields}
        self.assertTrue(
            {
                "document",
                "version_number",
                "storage_key",
                "original_filename",
                "mime_type",
                "file_size",
                "checksum",
                "uploaded_by",
                "metadata",
            }.issubset(fields)
        )
        self.assertIn(
            "uq_document_version_number",
            {c.name for c in DocumentVersion._meta.constraints},
        )

    def test_document_access_contract(self):
        from apps.documents.models import DocumentAccess

        fields = {f.name for f in DocumentAccess._meta.fields}
        self.assertTrue(
            {"document", "user", "is_active", "expires_at", "permission"}.issubset(
                fields
            )
        )

    def test_api_scope_and_workflow_contracts(self):
        list_src = Path("apps/documents/api/views/list_create.py").read_text(
            encoding="utf-8"
        )
        detail_src = Path(
            "apps/documents/api/views/retrieve_update_destroy.py"
        ).read_text(encoding="utf-8")
        version_src = Path(
            "apps/documents/workflows/document_version_creation.py"
        ).read_text(encoding="utf-8")
        for text in (list_src, detail_src):
            self.assertIn("tenant_id=tenant.id", text)
            self.assertIn("organization_id=organization.id", text)
            self.assertIn("organization.tenant_id", text)
        self.assertIn("context.actor_id", version_src)
        self.assertIn("uploaded_by=uploaded_by", version_src)
        self.assertIn("publish_after_commit", version_src)
        self.assertIn("dispatch_after_commit", version_src)

    def test_canonical_storage_boundary(self):
        source = Path(media.__file__).read_text(encoding="utf-8")
        self.assertIn("apps.common.storage", source)
        self.assertIn("get_storage_client", source)
        self.assertNotIn("class DocumentStorage", source)
