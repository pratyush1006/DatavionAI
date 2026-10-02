"""
Organization test factories.
"""

from __future__ import annotations

import factory

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationSize,
    OrganizationStatus,
    OrganizationType,
)
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.tests.factories import TenantFactory


class OrganizationFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for the canonical Organization model.

    Organizations are tenant-owned entities, so every generated
    organization receives a real canonical Tenant unless the caller
    explicitly supplies one.
    """

    class Meta:
        model = Organization

    class Params:
        """
        Non-model factory parameters.

        ``unique`` exists only inside Factory Boy and is never passed
        to the Organization model.
        """

        unique = factory.Sequence(
            lambda n: f"{n:08d}",
        )

    tenant = factory.SubFactory(
        TenantFactory,
    )

    name = factory.LazyAttribute(
        lambda obj: f"Apollo Hospital {obj.unique}",
    )

    display_name = factory.LazyAttribute(
        lambda obj: f"Apollo Hospital {obj.unique}",
    )

    code = factory.LazyAttribute(
        lambda obj: f"ORG{obj.unique}",
    )

    slug = factory.LazyAttribute(
        lambda obj: f"apollo-hospital-{obj.unique.lower()}",
    )

    category = OrganizationCategory.HEALTHCARE_PROVIDER

    organization_type = OrganizationType.HOSPITAL

    status = OrganizationStatus.ACTIVE

    size = OrganizationSize.SMALL

    email = factory.LazyAttribute(
        lambda obj: f"admin{obj.unique.lower()}@apollo.com",
    )

    support_email = factory.LazyAttribute(
        lambda obj: f"support{obj.unique.lower()}@apollo.com",
    )

    phone = ""

    website = "https://apollo.example.com"

    address = "MG Road"

    city = "Bangalore"

    state = "Karnataka"

    country = "India"

    postal_code = "560001"

    timezone = "Asia/Kolkata"

    registration_number = ""

    tax_number = ""

    license_number = ""

    accreditation = ""

    description = "Test organization."


def create_organization(
    **kwargs,
) -> Organization:
    """
    Create an organization for tests.
    """

    return OrganizationFactory(
        **kwargs,
    )


__all__ = (
    "OrganizationFactory",
    "create_organization",
)
