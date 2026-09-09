"""
Organization-scoped read selectors for Patient Relationships.

Selectors contain read/query concerns only. They do not perform
authorization, persistence, or workflow orchestration.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    VerificationStatus,
)
from apps.patient_management.relationships.models import PatientRelationship


class PatientRelationshipSelector:
    """Canonical read boundary for PatientRelationship."""

    @staticmethod
    def queryset(
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
    ) -> QuerySet[PatientRelationship]:
        queryset = PatientRelationship.objects.select_related(
            "organization",
            "patient",
            "related_patient",
        )

        if organization is not None:
            queryset = queryset.filter(organization=organization)
        elif organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)

        return queryset

    @classmethod
    def get(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
        relationship_id: UUID,
    ) -> PatientRelationship:
        return cls.queryset(
            organization=organization,
            organization_id=organization_id,
        ).get(id=relationship_id)

    get_by_id = get

    @classmethod
    def list(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
    ) -> QuerySet[PatientRelationship]:
        return cls.queryset(
            organization=organization,
            organization_id=organization_id,
        ).order_by("-is_primary", "-created_at")

    list_by_organization = list

    @classmethod
    def for_patient(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
        patient_id: UUID,
    ) -> QuerySet[PatientRelationship]:
        return (
            cls.queryset(
                organization=organization,
                organization_id=organization_id,
            )
            .filter(patient_id=patient_id)
            .order_by("-is_primary", "-created_at")
        )

    list_by_patient = for_patient

    @classmethod
    def get_primary(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
        patient_id: UUID,
    ) -> PatientRelationship | None:
        return (
            cls.for_patient(
                organization=organization,
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .filter(
                is_active=True,
                is_primary=True,
            )
            .first()
        )

    @classmethod
    def list_active(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
    ) -> QuerySet[PatientRelationship]:
        return cls.list(
            organization=organization,
            organization_id=organization_id,
        ).filter(
            is_active=True,
            status=RelationshipStatus.ACTIVE,
        )

    @classmethod
    def list_verified(
        cls,
        *,
        organization: Any | None = None,
        organization_id: UUID | None = None,
    ) -> QuerySet[PatientRelationship]:
        return cls.list(
            organization=organization,
            organization_id=organization_id,
        ).filter(
            verification_status=VerificationStatus.VERIFIED,
        )


get_patient_relationship = PatientRelationshipSelector.get
get_patient_relationship_for_patient = PatientRelationshipSelector.for_patient
list_patient_relationships = PatientRelationshipSelector.list


__all__ = (
    "PatientRelationshipSelector",
    "get_patient_relationship",
    "get_patient_relationship_for_patient",
    "list_patient_relationships",
)
