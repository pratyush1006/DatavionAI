"""
Documents workflow integration tests.
"""

from __future__ import annotations

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.core.workflows import WorkflowContext
from apps.documents.models import (
    Document,
    DocumentAccess,
    DocumentVersion,
)
from apps.documents.workflows import (
    DocumentCreationRequest,
    DocumentCreationWorkflow,
    DocumentDeletionRequest,
    DocumentDeletionWorkflow,
    DocumentUpdateRequest,
    DocumentUpdateWorkflow,
    DocumentVersionCreationRequest,
    DocumentVersionCreationWorkflow,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class DocumentWorkflowTestCase(
    TestCase,
):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(
            email="workflow@test.com",
            password="password123",
        )

        cls.tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
        )

        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Test Clinic",
            code="TEST001",
        )

        cls.context = WorkflowContext(
            actor_id=cls.user.id,
            tenant_id=cls.tenant.id,
        )

    def test_complete_document_lifecycle(self):

        create_result = DocumentCreationWorkflow(
            request=DocumentCreationRequest(
                organization_id=self.organization.id,
                title="Workflow Document",
                storage_key="workflow/document.pdf",
                document_type="medical_record",
                original_filename="document.pdf",
                mime_type="application/pdf",
                file_size=1000,
                checksum="workflow",
            )
        ).execute(context=self.context)

        self.assertTrue(create_result.success)

        document = Document.objects.get(title="Workflow Document")

        version_result = DocumentVersionCreationWorkflow(
            request=DocumentVersionCreationRequest(
                document_id=document.id,
                storage_key="workflow/document-v1.pdf",
                version_number=1,
                original_filename="v1.pdf",
                mime_type="application/pdf",
                file_size=2000,
                checksum="version",
            )
        ).execute(context=self.context)

        self.assertTrue(version_result.success)

        self.assertEqual(
            DocumentVersion.objects.count(),
            1,
        )

        update_result = DocumentUpdateWorkflow(
            request=DocumentUpdateRequest(
                document_id=document.id,
                data={
                    "title": "Updated Workflow Document",
                },
            )
        ).execute(context=self.context)

        self.assertTrue(update_result.success)

        access = DocumentAccess.objects.create(
            document=document,
            user=self.user,
            permission="view",
            is_active=True,
            expires_at=(timezone.now() + timedelta(days=1)),
        )

        self.assertTrue(access.is_active)

        delete_result = DocumentDeletionWorkflow(
            request=DocumentDeletionRequest(
                document_id=document.id,
            )
        ).execute(context=self.context)

        self.assertTrue(delete_result.success)

        document.refresh_from_db()

        self.assertEqual(
            document.status,
            "deleted",
        )
