"""Documents production contract tests."""

from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.documents.constants import DocumentVersionStatus
from apps.documents.models import Document, DocumentAccess, DocumentVersion
from apps.documents.services import (
    check_document_access,
    create_document_access,
    create_document_version,
    revoke_document_access,
)

User = get_user_model()

DOCUMENT_ACCESS_PERMISSION = (
    DocumentAccess._meta.get_field("permission").choices[0][0]
    if DocumentAccess._meta.get_field("permission").choices
    else None
)

if not DOCUMENT_ACCESS_PERMISSION:
    raise RuntimeError("Documents access permission vocabulary is empty.")


def make_tenant(suffix: str = "a"):
    from apps.platform.tenancy.models import Tenant

    return Tenant.objects.create(
        name=f"Documents Test Tenant {suffix}",
        slug=f"documents-test-tenant-{suffix}",
    )


def make_org(tenant, suffix: str = "a"):
    from apps.platform.organizations.models import Organization

    return Organization.objects.create(
        tenant=tenant,
        name=f"Documents Test Organization {suffix}",
        code=f"DOC{suffix.upper()}01",
        slug=f"documents-test-org-{suffix}",
    )


class DocumentsAccessProductionTests(TestCase):
    def setUp(self):
        self.tenant = make_tenant()
        self.organization = make_org(self.tenant)
        self.user = User.objects.create_user(
            email="documents-test-user@datavion.ai", password="TestPassword!123"
        )
        self.document = Document.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            title="Production Test Document",
            storage_key="documents/tests/production/document.pdf",
            original_filename="document.pdf",
            mime_type="application/pdf",
            file_size=10,
            checksum="sha256-production-test",
        )

    def test_grant_check_and_revoke(self):
        access = create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
        )
        self.assertIsInstance(access, DocumentAccess)
        self.assertTrue(access.is_active)
        self.assertTrue(
            check_document_access(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            )
        )
        revoke_document_access(access)
        self.assertFalse(
            check_document_access(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            )
        )

    def test_expired_access_is_denied(self):
        expired_at = timezone.now() - timedelta(seconds=1)
        DocumentAccess.objects.create(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
            expires_at=expired_at,
            is_active=True,
        )
        self.assertFalse(
            check_document_access(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            )
        )

    def test_future_access_is_allowed(self):
        create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        self.assertTrue(
            check_document_access(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            )
        )

    def test_regrant_reactivates_same_permission(self):
        first = create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
        )
        revoke_document_access(first)
        second = create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
        )
        self.assertEqual(first.pk, second.pk)
        self.assertTrue(second.is_active)
        self.assertEqual(
            DocumentAccess.objects.filter(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            ).count(),
            1,
        )

    def test_permission_vocabulary_is_model_canonical(self):
        field = DocumentAccess._meta.get_field("permission")
        allowed = {value for value, _label in field.choices}
        self.assertIn(DOCUMENT_ACCESS_PERMISSION, allowed)

    def test_duplicate_active_grant_is_reused(self):
        first = create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
        )
        second = create_document_access(
            document=self.document,
            user=self.user,
            permission=DOCUMENT_ACCESS_PERMISSION,
        )
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(
            DocumentAccess.objects.filter(
                document=self.document,
                user=self.user,
                permission=DOCUMENT_ACCESS_PERMISSION,
            ).count(),
            1,
        )


class DocumentsVersionProductionTests(TestCase):
    def setUp(self):
        self.tenant = make_tenant()
        self.organization = make_org(self.tenant)
        self.user = User.objects.create_user(
            email="documents-version-test@datavion.ai", password="TestPassword!123"
        )
        self.document = Document.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            title="Version Test Document",
            storage_key="documents/tests/production/version-root.pdf",
            original_filename="version-root.pdf",
            mime_type="application/pdf",
            file_size=10,
            checksum="root-checksum",
        )

    def test_first_version_is_current_one(self):
        version = create_document_version(
            document=self.document,
            storage_key="documents/tests/production/v1.pdf",
            checksum="checksum-v1",
            uploaded_by=self.user,
        )
        self.assertEqual(version.version_number, 1)
        self.assertEqual(version.status, DocumentVersionStatus.CURRENT)
        self.assertTrue(version.is_current)

    def test_new_version_supersedes_previous(self):
        first = create_document_version(
            document=self.document,
            storage_key="documents/tests/production/v1.pdf",
            checksum="checksum-v1",
            uploaded_by=self.user,
        )
        second = create_document_version(
            document=self.document,
            storage_key="documents/tests/production/v2.pdf",
            checksum="checksum-v2",
            uploaded_by=self.user,
        )
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(first.status, DocumentVersionStatus.SUPERSEDED)
        self.assertEqual(second.version_number, 2)
        self.assertEqual(second.status, DocumentVersionStatus.CURRENT)
        self.assertEqual(
            DocumentVersion.objects.filter(
                document=self.document, status=DocumentVersionStatus.CURRENT
            ).count(),
            1,
        )

    def test_empty_storage_key_rejected(self):
        with self.assertRaises(ValidationError):
            create_document_version(
                document=self.document, storage_key="", uploaded_by=self.user
            )


class DocumentsTenantBoundaryProductionTests(TestCase):
    def test_access_does_not_cross_documents(self):
        tenant_a = make_tenant("a")
        org_a = make_org(tenant_a, "a")
        tenant_b = make_tenant("b")
        org_b = make_org(tenant_b, "b")
        user = User.objects.create_user(
            email="documents-tenant-test@datavion.ai", password="TestPassword!123"
        )
        doc_a = Document.objects.create(
            tenant=tenant_a,
            organization=org_a,
            title="Tenant A",
            storage_key="documents/tests/a.pdf",
        )
        doc_b = Document.objects.create(
            tenant=tenant_b,
            organization=org_b,
            title="Tenant B",
            storage_key="documents/tests/b.pdf",
        )
        create_document_access(
            document=doc_a, user=user, permission=DOCUMENT_ACCESS_PERMISSION
        )
        self.assertTrue(
            check_document_access(
                document=doc_a, user=user, permission=DOCUMENT_ACCESS_PERMISSION
            )
        )
        self.assertFalse(
            check_document_access(
                document=doc_b, user=user, permission=DOCUMENT_ACCESS_PERMISSION
            )
        )
