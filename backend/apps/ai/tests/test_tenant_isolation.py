from __future__ import annotations

import pytest
from django.test import override_settings

from apps.ai.exceptions import AIAuthorizationError
from apps.ai.models import AIModuleReference, KnowledgeBase
from apps.ai.services.rag import add_text_document, index_document, retrieve
from apps.ai.services.registry import ensure_department_applications
from apps.ai.services.scope import (
    validate_application_scope,
    validate_document_scope,
    validate_knowledge_base_scope,
    validate_module_reference_scope,
    validate_scope,
)


@pytest.mark.django_db
def test_scope_rejects_cross_tenant_organization(tenant_factory, organization_factory):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)

    with pytest.raises(AIAuthorizationError):
        validate_scope(tenant=tenant_b, organization=organization_a)


@pytest.mark.django_db
def test_application_scope_rejects_cross_tenant_application(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    with pytest.raises(AIAuthorizationError):
        validate_application_scope(
            application,
            tenant=tenant_b,
            organization=organization_a,
        )


@pytest.mark.django_db
def test_module_reference_scope_rejects_cross_tenant_reference(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    reference = AIModuleReference.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        module_code="clinical.laboratories",
        resource_type="laboratory_order",
        resource_id="ORDER-A",
    )

    with pytest.raises(AIAuthorizationError):
        validate_module_reference_scope(
            reference,
            tenant=tenant_b,
            organization=organization_b,
        )


@pytest.mark.django_db
def test_knowledge_base_scope_rejects_cross_tenant_access(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    knowledge_base = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application,
        name="Tenant A Knowledge",
    )

    with pytest.raises(AIAuthorizationError):
        validate_knowledge_base_scope(
            knowledge_base,
            tenant=tenant_b,
            organization=organization_b,
        )


@pytest.mark.django_db
def test_rag_retrieve_rejects_cross_tenant_access(tenant_factory, organization_factory):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    knowledge_base = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application,
        name="Tenant A Knowledge",
    )

    with pytest.raises(AIAuthorizationError):
        retrieve(
            knowledge_base=knowledge_base,
            tenant=tenant_b,
            organization=organization_b,
            query="secret",
            top_k=5,
        )


@pytest.mark.django_db
def test_rag_document_write_rejects_cross_tenant_access(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    knowledge_base = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application,
        name="Tenant A Knowledge",
    )

    with pytest.raises(AIAuthorizationError):
        add_text_document(
            knowledge_base=knowledge_base,
            tenant=tenant_b,
            organization=organization_b,
            title="Cross Tenant",
            content="must never be written",
        )


@pytest.mark.django_db
def test_rag_index_rejects_cross_tenant_access(tenant_factory, organization_factory):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    knowledge_base = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application,
        name="Tenant A Knowledge",
    )

    document = add_text_document(
        knowledge_base=knowledge_base,
        tenant=tenant_a,
        organization=organization_a,
        title="Tenant A",
        content="tenant a protected content",
    )

    with pytest.raises(AIAuthorizationError):
        index_document(
            document=document,
            tenant=tenant_b,
            organization=organization_b,
        )


@pytest.mark.django_db
def test_document_scope_rejects_cross_tenant_document(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]

    knowledge_base = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application,
        name="Tenant A Knowledge",
    )

    document = add_text_document(
        knowledge_base=knowledge_base,
        tenant=tenant_a,
        organization=organization_a,
        title="Tenant A",
        content="tenant a protected content",
    )

    with pytest.raises(AIAuthorizationError):
        validate_document_scope(
            document,
            tenant=tenant_b,
            organization=organization_b,
        )


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="mock",
    AI_EMBEDDING_PROVIDER="mock",
    AI_ALLOW_MOCK_PROVIDER=True,
)
def test_rag_results_cannot_cross_requested_tenant_scope(
    tenant_factory, organization_factory
):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization_a = organization_factory(tenant=tenant_a)
    organization_b = organization_factory(tenant=tenant_b)

    application_a = ensure_department_applications(
        tenant=tenant_a,
        organization=organization_a,
    )[0]
    application_b = ensure_department_applications(
        tenant=tenant_b,
        organization=organization_b,
    )[0]

    kb_a = KnowledgeBase.objects.create(
        tenant=tenant_a,
        organization=organization_a,
        application=application_a,
        name="A Knowledge",
    )
    kb_b = KnowledgeBase.objects.create(
        tenant=tenant_b,
        organization=organization_b,
        application=application_b,
        name="B Knowledge",
    )

    doc_a = add_text_document(
        knowledge_base=kb_a,
        tenant=tenant_a,
        organization=organization_a,
        title="A Secret",
        content="alpha tenant private content",
    )
    doc_b = add_text_document(
        knowledge_base=kb_b,
        tenant=tenant_b,
        organization=organization_b,
        title="B Secret",
        content="beta tenant private content",
    )

    index_document(
        document=doc_a,
        tenant=tenant_a,
        organization=organization_a,
    )
    index_document(
        document=doc_b,
        tenant=tenant_b,
        organization=organization_b,
    )

    results_a = retrieve(
        knowledge_base=kb_a,
        tenant=tenant_a,
        organization=organization_a,
        query="private content",
        top_k=10,
    )

    assert results_a
    assert all(item["document_id"] != str(doc_b.uuid) for item in results_a)
    assert all("beta tenant" not in item["content"] for item in results_a)
