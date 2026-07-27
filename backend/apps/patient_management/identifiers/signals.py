"""
Signals for the Identifiers module.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.patient_management.identifiers.models import (
    IdentifierVerification,
    PatientIdentifier,
)


@receiver(
    post_save,
    sender=IdentifierVerification,
)
def sync_identifier_verification(
    sender: type[IdentifierVerification],
    instance: IdentifierVerification,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Synchronize the latest verification state with the identifier.
    """
    if not created:
        return

    identifier = instance.identifier
    identifier.verification_status = instance.status
    identifier.verified_by = instance.verified_by
    identifier.verified_at = instance.verified_at
    identifier.save(
        update_fields=[
            "verification_status",
            "verified_by",
            "verified_at",
            "updated_at",
        ],
    )


@receiver(
    post_save,
    sender=PatientIdentifier,
)
def ensure_single_primary_identifier(
    sender: type[PatientIdentifier],
    instance: PatientIdentifier,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Ensure only one primary identifier exists for a patient and identifier type.
    """
    if not instance.is_primary:
        return

    (
        PatientIdentifier.objects.filter(
            patient=instance.patient,
            identifier_type=instance.identifier_type,
            is_primary=True,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            is_primary=False,
        )
    )
