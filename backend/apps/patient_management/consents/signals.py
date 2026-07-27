"""
Signals for the Patient Consents module.
"""

from __future__ import annotations

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.patient_management.consents.constants import (
    ConsentStatus,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)


@receiver(
    pre_save,
    sender=PatientConsent,
)
def ensure_single_active_consent(
    sender,
    instance: PatientConsent,
    **kwargs,
) -> None:
    """
    Ensure that only one active consent exists for a patient,
    organization, and consent type.
    """
    if instance.status != ConsentStatus.ACTIVE:
        return

    (
        sender.objects.filter(
            organization=instance.organization,
            patient=instance.patient,
            consent_type=instance.consent_type,
            status=ConsentStatus.ACTIVE,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            status=ConsentStatus.REVOKED,
        )
    )
