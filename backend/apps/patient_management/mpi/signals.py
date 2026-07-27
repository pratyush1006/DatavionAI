"""
Signals for the Master Patient Index module.
"""

from __future__ import annotations

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(
    post_save,
    sender=MasterPatientIndex,
)
def ensure_single_active_mpi(
    sender: type[MasterPatientIndex],
    instance: MasterPatientIndex,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Ensure a patient has only one active MPI record.
    """

    if not created:
        return

    (
        MasterPatientIndex.objects.filter(
            patient=instance.patient,
            status=instance.status,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            status="inactive",
        )
    )
