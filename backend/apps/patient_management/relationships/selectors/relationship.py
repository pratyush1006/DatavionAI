"""
Selectors for Patient Relationships.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


def get_relationship_by_id(
    relationship_id: int,
) -> PatientRelationship:
    """
    Return a relationship by its primary key.
    """
    return PatientRelationship.objects.get(
        pk=relationship_id,
    )


def get_patient_relationships(
    *,
    patient_id: int,
) -> QuerySet[PatientRelationship]:
    """
    Return all relationships for a patient.
    """
    return (
        PatientRelationship.objects.select_related(
            "organization",
            "patient",
            "related_patient",
        )
        .filter(
            patient_id=patient_id,
        )
        .order_by(
            "-is_primary",
            "relationship_type",
        )
    )


def get_primary_relationship(
    *,
    patient_id: int,
    relationship_type: str,
) -> PatientRelationship | None:
    """
    Return the primary relationship for a patient.
    """
    return (
        PatientRelationship.objects.select_related(
            "organization",
            "patient",
            "related_patient",
        )
        .filter(
            patient_id=patient_id,
            relationship_type=relationship_type,
            is_primary=True,
        )
        .first()
    )


def get_relationships_by_type(
    *,
    organization_id: int,
    relationship_type: str,
) -> QuerySet[PatientRelationship]:
    """
    Return relationships by type.
    """
    return (
        PatientRelationship.objects.select_related(
            "organization",
            "patient",
            "related_patient",
        )
        .filter(
            organization_id=organization_id,
            relationship_type=relationship_type,
        )
        .order_by(
            "-created_at",
        )
    )


__all__ = [
    "get_patient_relationships",
    "get_primary_relationship",
    "get_relationship_by_id",
    "get_relationships_by_type",
]
