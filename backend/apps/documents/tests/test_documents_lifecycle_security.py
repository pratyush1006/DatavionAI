"""Documents lifecycle/security production contract tests."""

from __future__ import annotations

from unittest.mock import patch
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.documents.models import Document
from apps.documents.selectors import get_document_by_id_for_tenant, get_documents
from apps.documents.services import delete_document, update_document


def make_document(suffix: str = "a"):
    from apps.platform.organizations.models import Organization
    from apps.platform.tenancy.models import Tenant

    tenant = Tenant.objects.create(
        name=f"Documents Lifecycle Test Tenant {suffix}",
        slug=f"documents-lifecycle-test-tenant-{suffix}",
    )
    organization = Organization.objects.create(
        tenant=tenant,
        name=f"Documents Lifecycle Test Organization {suffix}",
        code=f"DLS{suffix.upper()}01",
        slug=f"documents-lifecycle-test-org-{suffix}",
    )
    document = Document.objects.create(
        tenant=tenant,
        organization=organization,
        title="Production document",
        storage_key=f"documents/lifecycle/{uuid4()}",
        document_type="general",
    )
    return document, tenant, organization


class DocumentSelectorSecurityTests(TestCase):
    def test_tenant_scoped_lookup_cannot_cross_tenant(self):
        document_a, tenant_a, _ = make_document("a")
        document_b, tenant_b, _ = make_document("b")
        self.assertEqual(
            get_document_by_id_for_tenant(
                document_id=document_a.id, tenant_id=tenant_a.id
            ).id,
            document_a.id,
        )
        with self.assertRaises(Document.DoesNotExist):
            get_document_by_id_for_tenant(
                document_id=document_a.id, tenant_id=tenant_b.id
            )
        ids = set(get_documents(tenant_id=tenant_a.id).values_list("id", flat=True))
        self.assertIn(document_a.id, ids)
        self.assertNotIn(document_b.id, ids)


class DocumentServiceSecurityTests(TestCase):
    def test_empty_update_rejected(self):
        document, _, _ = make_document("empty")
        with self.assertRaises(ValidationError):
            update_document(instance=document, data={})

    def test_unknown_field_rejected(self):
        document, _, _ = make_document("unknown")
        with self.assertRaises(ValidationError):
            update_document(instance=document, data={"tenant_id": uuid4()})

    def test_deleted_document_cannot_update(self):
        document, _, _ = make_document("deleted")
        delete_document(instance=document)
        with self.assertRaises(ValidationError):
            update_document(instance=document, data={"title": "must fail"})

    def test_delete_is_soft_and_idempotent(self):
        document, _, _ = make_document("softdelete")
        first = delete_document(instance=document)
        second = delete_document(instance=first)
        self.assertEqual(str(first.status), "deleted")
        self.assertEqual(str(second.status), "deleted")
        self.assertEqual(Document.objects.filter(id=document.id).count(), 1)


class DocumentRBACAdapterTests(TestCase):
    def test_document_permission_is_organization_and_tenant_scoped(self):
        from apps.documents.permissions import CanViewDocument

        _document, tenant, organization = make_document("rbac")
        permission = CanViewDocument()

        class Request:
            user = type("User", (), {"is_authenticated": True})()

        class View:
            current_tenant = tenant
            current_organization = organization

        with patch(
            "apps.documents.permissions.document.user_has_permission",
            return_value=True,
        ) as check:
            self.assertTrue(permission.has_permission(Request(), View()))
            check.assert_called_once_with(
                user=Request.user,
                permission="documents.view",
                organization=organization,
            )

        View.current_tenant = type("Tenant", (), {"id": uuid4()})()
        self.assertFalse(permission.has_permission(Request(), View()))

    def test_document_permission_denies_missing_context(self):
        from apps.documents.permissions import CanViewDocument

        permission = CanViewDocument()

        class Request:
            user = type("User", (), {"is_authenticated": True})()

        class View:
            current_tenant = None
            current_organization = None

        self.assertFalse(permission.has_permission(Request(), View()))
