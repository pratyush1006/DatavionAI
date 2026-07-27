"""
Signals for the Family Members module.
"""

from __future__ import annotations

from django.db.models.signals import (
    post_save,
    pre_save,
)
from django.dispatch import receiver

from apps.patient_management.family_members.models import (
    FamilyMember,
)

__all__ = []


@receiver(
    pre_save,
    sender=FamilyMember,
)
def ensure_single_next_of_kin(
    sender,
    instance: FamilyMember,
    **kwargs,
) -> None:
    """
    Ensure only one next of kin exists for a patient.
    """
    if not instance.is_next_of_kin or instance.pk is None:
        return

    FamilyMember.objects.filter(
        patient=instance.patient,
        is_next_of_kin=True,
    ).exclude(
        id=instance.id,
    ).update(
        is_next_of_kin=False,
    )


@receiver(
    post_save,
    sender=FamilyMember,
)
def synchronize_emergency_contact(
    sender,
    instance: FamilyMember,
    created: bool,
    **kwargs,
) -> None:
    """
    Hook for synchronizing Family Member with the
    Emergency Contact module.

    Currently this signal is intentionally left as a
    placeholder so the integration can be implemented
    without modifying the model layer.
    """
    del sender
    del instance
    del created
    del kwargs
