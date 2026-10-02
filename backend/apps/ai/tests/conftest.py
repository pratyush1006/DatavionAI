"""Local AI test factories with lazy project imports."""

from __future__ import annotations

import pytest


@pytest.fixture
def tenant_factory(db):
    from apps.platform.tenancy.models import Tenant

    counter = {"n": 0}

    def make(**kwargs):
        counter["n"] += 1
        return Tenant.objects.create(
            name=kwargs.pop("name", f"AI Tenant {counter['n']}"),
            slug=kwargs.pop("slug", f"ai-tenant-{counter['n']}"),
            **kwargs,
        )

    return make


@pytest.fixture
def organization_factory(db):
    from apps.platform.organizations.models import Organization

    counter = {"n": 0}

    def make(*, tenant, **kwargs):
        counter["n"] += 1
        return Organization.objects.create(
            tenant=tenant,
            name=kwargs.pop("name", f"AI Organization {counter['n']}"),
            code=kwargs.pop("code", f"AIO{counter['n']:03d}"),
            **kwargs,
        )

    return make
