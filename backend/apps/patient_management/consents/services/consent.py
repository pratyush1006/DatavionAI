"""
Business services for the Patient Consents module.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.patient_management.consents.constants import (
    ConsentStatus,
)
from apps.patient_management.consents.models import Consent

__all__ = [
    "create_consent",
    "expire_consent",
    "grant_consent",
    "revoke_consent",
    "update_consent",
    "withdraw_consent",
]


@transaction.atomic
def create_consent(
    **validated_data,
) -> Consent:
    """
    Create a consent.
    """

    return Consent.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_consent(
    consent: Consent,
    **validated_data,
) -> Consent:
    """
    Update a consent.
    """

    for field, value in validated_data.items():
        setattr(
            consent,
            field,
            value,
        )

    consent.save(
        update_fields=list(
            validated_data.keys(),
        ),
    )

    return consent


@transaction.atomic
def grant_consent(
    consent: Consent,
) -> Consent:
    """
    Grant a consent.
    """

    consent.status = ConsentStatus.GRANTED
    consent.granted_at = timezone.now()
    consent.save(
        update_fields=[
            "status",
            "granted_at",
        ],
    )

    return consent


@transaction.atomic
def revoke_consent(
    consent: Consent,
) -> Consent:
    """
    Revoke a consent.
    """

    consent.status = ConsentStatus.REVOKED
    consent.revoked_at = timezone.now()
    consent.is_active = False

    consent.save(
        update_fields=[
            "status",
            "revoked_at",
            "is_active",
        ],
    )

    return consent


@transaction.atomic
def withdraw_consent(
    consent: Consent,
) -> Consent:
    """
    Withdraw a consent.
    """

    consent.status = ConsentStatus.WITHDRAWN
    consent.withdrawn_at = timezone.now()
    consent.is_active = False

    consent.save(
        update_fields=[
            "status",
            "withdrawn_at",
            "is_active",
        ],
    )

    return consent


@transaction.atomic
def expire_consent(
    consent: Consent,
) -> Consent:
    """
    Expire a consent.
    """

    consent.status = ConsentStatus.EXPIRED
    consent.is_active = False

    consent.save(
        update_fields=[
            "status",
            "is_active",
        ],
    )

    return consent
