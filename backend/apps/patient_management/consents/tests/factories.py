"""
Factories for the Patient Consents module.
"""

from __future__ import annotations

import factory

from apps.patient_management.consents.constants import (
    ConsentMethod,
    ConsentSource,
    ConsentStatus,
    ConsentType,
)
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.patients.tests.factories import (
    PatientFactory,
)
from apps.platform.organizations.tests.factories import (
    OrganizationFactory,
)

__all__ = [
    "ConsentFactory",
]


class ConsentFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Consent.
    """

    class Meta:
        model = Consent

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )

    consent_number = factory.Sequence(
        lambda n: f"CONSENT-{n:06d}",
    )

    title = factory.Sequence(
        lambda n: f"Treatment Consent {n}",
    )

    description = factory.Faker(
        "paragraph",
    )

    consent_type = ConsentType.TREATMENT

    status = ConsentStatus.DRAFT

    method = ConsentMethod.DIGITAL

    source = ConsentSource.RECEPTION

    version = 1

    is_required = False

    is_active = True
