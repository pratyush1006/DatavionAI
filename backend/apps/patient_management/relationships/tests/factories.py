"""
Factories for the Patient Relationships module.
"""

from __future__ import annotations

import factory

from apps.patient_management.relationships.constants import (
    RelationshipSource,
    RelationshipStatus,
    RelationshipType,
    RelationshipVerificationStatus,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipFactory(
    factory.django.DjangoModelFactory,
):
    """Factory for PatientRelationship."""

    class Meta:
        model = PatientRelationship

    organization = factory.SubFactory(
        "apps.organizations.tests.factories.OrganizationFactory",
    )

    patient = factory.SubFactory(
        "apps.patient_management.patients.tests.factories.PatientFactory",
    )

    related_patient = factory.SubFactory(
        "apps.patient_management.patients.tests.factories.PatientFactory",
    )

    relationship_type = RelationshipType.GUARDIAN
    relationship_name = ""
    relationship_strength = 5

    status = RelationshipStatus.ACTIVE

    verification_status = RelationshipVerificationStatus.PENDING

    source = RelationshipSource.MANUAL

    is_primary = False

    start_date = None
    end_date = None

    notes = ""
