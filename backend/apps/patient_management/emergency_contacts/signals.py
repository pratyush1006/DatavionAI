"""
Signals for the Emergency Contacts module.
"""

from __future__ import annotations

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import EmergencyContact


@receiver(
    post_save,
    sender=EmergencyContact,
)
def emergency_contact_saved(
    sender,
    instance,
    created,
    **kwargs,
):
    """
    Handle emergency contact save.

    Reserved for future:
    - Audit logging
    - Notification events
    - Event bus publishing
    """
    return


@receiver(
    post_delete,
    sender=EmergencyContact,
)
def emergency_contact_deleted(
    sender,
    instance,
    **kwargs,
):
    """
    Handle emergency contact deletion.

    Reserved for future:
    - Audit logging
    - Event bus
    """
    return
