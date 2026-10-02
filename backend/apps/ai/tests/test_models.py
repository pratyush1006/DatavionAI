"""AI model and tenant isolation tests."""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from apps.ai.models import AIApplication


@pytest.mark.django_db
def test_application_clean_rejects_cross_tenant(tenant_factory, organization_factory):
    tenant_a = tenant_factory()
    tenant_b = tenant_factory()
    organization = organization_factory(tenant=tenant_a)
    application = AIApplication(
        tenant=tenant_b, organization=organization, code="X", name="X"
    )
    with pytest.raises(ValidationError):
        application.full_clean()
