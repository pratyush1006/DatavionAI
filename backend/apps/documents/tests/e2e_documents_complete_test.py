"""
DatavionOS Documents Complete E2E Test.

Covers:

- User authentication
- Tenant context
- Organization context
- RBAC permission
- Create document workflow
- Create version workflow
- Update workflow
- Delete workflow
- Document access lifecycle
"""

from __future__ import annotations

from datetime import timedelta

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
from apps.platform.rbac.engines import user_has_permission


def run_documents_complete_e2e():

    print("=" * 90)
    print("DatavionOS DOCUMENTS COMPLETE E2E TEST")
    print("=" * 90)

    # -------------------------------------------------
    # USER CONTEXT
    # -------------------------------------------------

    user = User.objects.get(email="admin@datavion.ai")

    organization = user.organization_roles.first().organization

    tenant = organization.tenant

    print("\nUSER")
    print(user.email)

    print("\nORGANIZATION")
    print(organization.name)

    print("\nTENANT")
    print(tenant.name)

    # -------------------------------------------------
    # RBAC
    # -------------------------------------------------

    assert user_has_permission(
        user=user,
        permission="documents.create",
        organization=organization,
    )

    print("\nRBAC")
    print("PASS")

    context = WorkflowContext(
        actor_id=user.id,
        tenant_id=tenant.id,
    )

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    create_request = DocumentCreationRequest(
        organization_id=organization.id,
        title="Complete E2E Patient Document",
        storage_key="documents/e2e/test.pdf",
        document_type="medical_record",
        original_filename="test.pdf",
        mime_type="application/pdf",
        file_size=1024,
        checksum="e2e-checksum",
        metadata={
            "test": True,
        },
    )

    create_result = DocumentCreationWorkflow(request=create_request).execute(
        context=context
    )

    assert create_result.success

    document = Document.objects.filter(title="Complete E2E Patient Document").latest(
        "created_at"
    )

    print("\nCREATE")
    print(create_result.code)
    print(document.id)

    # -------------------------------------------------
    # VERSION
    # -------------------------------------------------

    version_request = DocumentVersionCreationRequest(
        document_id=document.id,
        storage_key="documents/e2e/test-v1.pdf",
        version_number=1,
        original_filename="test-v1.pdf",
        mime_type="application/pdf",
        file_size=2048,
        checksum="version-checksum",
    )

    version_result = DocumentVersionCreationWorkflow(request=version_request).execute(
        context=context
    )

    assert version_result.success

    print("\nVERSION")
    print(version_result.code)

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    update_request = DocumentUpdateRequest(
        document_id=document.id,
        data={"title": "Updated Complete E2E Document"},
    )

    update_result = DocumentUpdateWorkflow(request=update_request).execute(
        context=context
    )

    assert update_result.success

    print("\nUPDATE")
    print(update_result.code)

    # -------------------------------------------------
    # ACCESS
    # -------------------------------------------------

    access = DocumentAccess.objects.create(
        document=document,
        user=user,
        permission="view",
        is_active=True,
        expires_at=(timezone.now() + timedelta(days=1)),
        metadata={"source": "e2e"},
    )

    assert access.id

    print("\nACCESS")
    print("CREATED")

    assert DocumentAccess.objects.filter(
        id=access.id,
        is_active=True,
    ).exists()

    print("ACCESS CHECK")
    print("PASS")

    access.is_active = False

    access.save(update_fields=["is_active"])

    print("ACCESS REVOKE")
    print("PASS")

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------

    delete_request = DocumentDeletionRequest(document_id=document.id)

    delete_result = DocumentDeletionWorkflow(request=delete_request).execute(
        context=context
    )

    assert delete_result.success

    document.refresh_from_db()

    assert document.is_deleted is True

    print("\nDELETE")
    print(delete_result.code)

    # -------------------------------------------------
    # FINAL DATABASE CHECK
    # -------------------------------------------------

    print("\nDATABASE")

    print("Documents:", Document.objects.count())

    print("Versions:", DocumentVersion.objects.count())

    print("Access:", DocumentAccess.objects.count())

    print()
    print("=" * 90)
    print("DOCUMENTS COMPLETE E2E TEST PASSED")
    print("=" * 90)


run_documents_complete_e2e()
