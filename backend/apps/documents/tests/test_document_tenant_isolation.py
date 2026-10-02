"""
Document tenant isolation tests.

Validates SaaS data boundary:

Tenant A
    |
    Organization A
        |
        Document A


Tenant B
    |
    Organization B
        |
        Document B
"""

from __future__ import annotations

from django.test import TestCase

from apps.core.workflows import WorkflowContext
from apps.documents.models import Document
from apps.documents.workflows import (
    DocumentCreationRequest,
    DocumentCreationWorkflow,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class DocumentTenantIsolationTestCase(
    TestCase,
):
    @classmethod
    def setUpTestData(
        cls,
    ):

        cls.user_a = User.objects.create_user(
            email="tenant_a@test.com",
            password="password123",
        )

        cls.user_b = User.objects.create_user(
            email="tenant_b@test.com",
            password="password123",
        )

        cls.tenant_a = Tenant.objects.create(
            name="Tenant A",
            slug="tenant-a",
        )

        cls.tenant_b = Tenant.objects.create(
            name="Tenant B",
            slug="tenant-b",
        )

        cls.organization_a = Organization.objects.create(
            tenant=cls.tenant_a,
            name="Organization A",
            code="ORGA",
        )

        cls.organization_b = Organization.objects.create(
            tenant=cls.tenant_b,
            name="Organization B",
            code="ORGB",
        )

    def test_document_isolation_between_tenants(
        self,
    ):

        context_a = WorkflowContext(
            actor_id=self.user_a.id,
            tenant_id=self.tenant_a.id,
        )

        result = DocumentCreationWorkflow(
            request=DocumentCreationRequest(
                organization_id=self.organization_a.id,
                title="Tenant A Document",
                storage_key="tenant-a/document.pdf",
                document_type="medical_record",
                original_filename="document.pdf",
                mime_type="application/pdf",
                file_size=100,
                checksum="tenant-a",
            ),
        ).execute(
            context=context_a,
        )

        self.assertTrue(
            result.success,
        )

        document_a = Document.objects.get(
            title="Tenant A Document",
        )

        self.assertEqual(
            document_a.tenant_id,
            self.tenant_a.id,
        )

        # Tenant B cannot see Tenant A document

        tenant_b_documents = Document.objects.filter(
            tenant=self.tenant_b,
        )

        self.assertFalse(
            tenant_b_documents.filter(
                id=document_a.id,
            ).exists(),
        )
