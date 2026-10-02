"""
Tenant test factories.

Canonical test factory infrastructure for the DatavionOS
platform tenancy bounded context.
"""

from __future__ import annotations

import factory

from apps.platform.tenancy.models import Tenant


class TenantFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for the canonical Tenant model.

    Tenant is the root SaaS isolation boundary. Organizations,
    accounts, subscriptions, and other tenant-owned entities
    should reference a Tenant created by this factory in tests.
    """

    class Meta:
        model = Tenant

    name = factory.Sequence(
        lambda n: f"Datavion Test Tenant {n}",
    )

    slug = factory.Sequence(
        lambda n: f"datavion-test-tenant-{n}",
    )


def create_tenant(
    **kwargs,
) -> Tenant:
    """
    Create and persist a Tenant for tests.
    """

    return TenantFactory(
        **kwargs,
    )


__all__ = (
    "TenantFactory",
    "create_tenant",
)
