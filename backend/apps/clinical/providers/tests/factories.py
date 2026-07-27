"""
Factories for provider tests.
"""

from __future__ import annotations

import factory

from apps.clinical.providers.constants import (
    DEFAULT_PROVIDER_STATUS,
    ProviderType,
)
from apps.clinical.providers.models import Provider
from apps.organization.employees.tests.factories import (
    EmployeeFactory,
)
from apps.platform.organizations.tests.factories import (
    OrganizationFactory,
)


class ProviderFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Provider.
    """

    class Meta:
        model = Provider

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    employee = factory.SubFactory(
        EmployeeFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )

    provider_number = factory.Sequence(
        lambda n: f"PRV-{n:06d}",
    )

    license_number = factory.Sequence(
        lambda n: f"LIC-{n:08d}",
    )

    provider_type = ProviderType.PHYSICIAN

    years_of_experience = 5

    is_accepting_patients = True

    bio = factory.Faker(
        "paragraph",
        nb_sentences=3,
    )

    status = DEFAULT_PROVIDER_STATUS

    is_active = True


__all__ = [
    "ProviderFactory",
]
