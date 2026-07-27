"""
Signals for the Contacts module.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.patient_management.contacts.models import Contact


@receiver(
    post_save,
    sender=Contact,
)
def ensure_single_primary_contact(
    sender: type[Contact],
    instance: Contact,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Ensure only one primary contact exists for a patient and contact type.
    """
    if not instance.is_primary:
        return

    (
        Contact.objects.filter(
            patient=instance.patient,
            contact_type=instance.contact_type,
            is_primary=True,
        )
        .exclude(
            pk=instance.pk,
        )
        .update(
            is_primary=False,
        )
    )
