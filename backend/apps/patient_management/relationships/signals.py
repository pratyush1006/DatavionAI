"""
Signals for the Patient Relationships module.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


@receiver(
    post_save,
    sender=PatientRelationship,
)
def ensure_single_primary_relationship(
    sender: type[PatientRelationship],
    instance: PatientRelationship,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Ensure only one primary relationship exists for a patient
    and relationship type.
    """
    if not instance.is_primary:
        return

    (
        PatientRelationship.objects.filter(
            patient=instance.patient,
            relationship_type=instance.relationship_type,
            is_primary=True,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            is_primary=False,
        )
    )
