"""
Organization test factories.
"""

from __future__ import annotations

import uuid

import factory

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationSize,
    OrganizationStatus,
    OrganizationType,
)
from apps.platform.organizations.models import (
    Organization,
)


class OrganizationFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Organization model.
    """

    class Meta:
        model = Organization

    unique = factory.LazyFunction(
        lambda: uuid.uuid4().hex[:8].upper(),
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
    Create organization for tests.
    """

    return OrganizationFactory(
        **kwargs,
    )


__all__ = [
    "OrganizationFactory",
    "create_organization",
]
