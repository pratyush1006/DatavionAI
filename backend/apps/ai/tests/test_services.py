"""AI service integration tests."""

from __future__ import annotations

import pytest
from django.test import override_settings

from apps.ai.models import KnowledgeBase
from apps.ai.services.chat import generate
from apps.ai.services.rag import add_text_document, index_document, retrieve
from apps.ai.services.registry import ensure_department_applications


@pytest.mark.django_db
def test_department_registry(tenant_factory, organization_factory):
    tenant = tenant_factory()
    organization = organization_factory(tenant=tenant)
    applications = ensure_department_applications(
        tenant=tenant, organization=organization
    )
    assert {x.code for x in applications} == {
        "CLINICAL_AI",
        "LABORATORY_AI",
        "PHARMACY_AI",
        "IMAGING_AI",
        "REVENUE_CYCLE_AI",
    }


@pytest.mark.django_db
@override_settings(AI_PROVIDER="mock", AI_ALLOW_MOCK_PROVIDER=True)
def test_chat_records_usage(tenant_factory, organization_factory):
    tenant = tenant_factory()
    organization = organization_factory(tenant=tenant)
    application = ensure_department_applications(
        tenant=tenant, organization=organization
    )[0]
    from apps.ai.models import AIModuleReference

    module_reference = AIModuleReference.objects.create(
        tenant=tenant,
        organization=organization,
        module_code="tests",
        resource_type="test",
        resource_id="chat",
    )
    response = generate(
        application=application,
        tenant=tenant,
        organization=organization,
        module_reference=module_reference,
        messages=[{"role": "user", "content": "hello"}],
    )
    assert response.content
    assert application.requests.filter(status="succeeded").count() == 1
    assert application.requests.first().usage.total_tokens > 0


@pytest.mark.django_db
@override_settings(
    AI_PROVIDER="mock",
    AI_EMBEDDING_PROVIDER="mock",
    AI_ALLOW_MOCK_PROVIDER=True,
)
def test_rag_index_and_retrieve(tenant_factory, organization_factory):
    tenant = tenant_factory()
    organization = organization_factory(tenant=tenant)
    application = ensure_department_applications(
        tenant=tenant, organization=organization
    )[0]
    kb = KnowledgeBase.objects.create(
        tenant=tenant,
        organization=organization,
        application=application,
        name="Clinical Knowledge",
    )
    document = add_text_document(
        knowledge_base=kb,
        tenant=tenant,
        organization=organization,
        title="Test",
        content="patient laboratory result is normal",
    )
    assert (
        index_document(document=document, tenant=tenant, organization=organization) > 0
    )
    results = retrieve(
        knowledge_base=kb,
        tenant=tenant,
        organization=organization,
        query="laboratory result",
        top_k=1,
    )
    assert results and results[0]["content"]
