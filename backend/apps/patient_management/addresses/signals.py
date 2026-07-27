"""
Signals for the Addresses module.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.patient_management.addresses.models import Address


@receiver(
    post_save,
    sender=Address,
)
def ensure_single_primary_address(
    sender: type[Address],
    instance: Address,
    created: bool,
    **kwargs: object,
) -> None:
    """Ensure only one primary address exists."""

    if not instance.is_primary:
        return

    (
        Address.objects.filter(
            patient=instance.patient,
            address_type=instance.address_type,
            is_primary=True,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            is_primary=False,
        )
    )
