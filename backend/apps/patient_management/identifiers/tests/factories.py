"""
Factories for the Patient Identifiers module.
"""

from __future__ import annotations

import factory

from apps.patient_management.identifiers.constants import (
    IdentifierPriority,
    IdentifierSource,
    IdentifierStatus,
    IdentifierType,
    VerificationStatus,
)
from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierFactory(factory.django.DjangoModelFactory):
    """Factory for PatientIdentifier."""

    class Meta:
        model = PatientIdentifier

    organization = factory.SubFactory(
        "apps.organizations.tests.factories.OrganizationFactory",
    )
    patient = factory.SubFactory(
        "apps.patient_management.tests.factories.PatientFactory",
    )

    identifier_type = IdentifierType.MRN
    identifier_value = factory.Sequence(
        lambda n: f"MRN{100000 + n}",
    )
    display_value = factory.SelfAttribute(
        "identifier_value",
    )

    priority = IdentifierPriority.PRIMARY
    status = IdentifierStatus.ACTIVE
    verification_status = VerificationStatus.PENDING
    source = IdentifierSource.REGISTRATION
    is_primary = True
