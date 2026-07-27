"""
Services for the Emergency Contacts module.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from ..models import EmergencyContact


class EmergencyContactService:
    """
    Emergency Contact service.
    """

    @classmethod
    @transaction.atomic
    def create(
        cls,
        **validated_data,
    ) -> EmergencyContact:

        if validated_data.get(
            "is_primary",
        ):
            EmergencyContact.objects.filter(
                patient=validated_data["patient"],
                is_primary=True,
            ).update(
                is_primary=False,
            )

        return EmergencyContact.objects.create(
            **validated_data,
        )

    @classmethod
    @transaction.atomic
    def update(
        cls,
        instance: EmergencyContact,
        **validated_data,
    ) -> EmergencyContact:

        if validated_data.get(
            "is_primary",
        ):
            EmergencyContact.objects.filter(
                patient=instance.patient,
                is_primary=True,
            ).exclude(
                pk=instance.pk,
            ).update(
                is_primary=False,
            )

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def verify(
        cls,
        instance: EmergencyContact,
        user,
    ) -> EmergencyContact:

        instance.is_verified = True
        instance.verified_at = timezone.now()
        instance.verified_by = user

        instance.save(
            update_fields=[
                "is_verified",
                "verified_at",
                "verified_by",
            ],
        )

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        instance: EmergencyContact,
    ) -> None:

        instance.delete()
