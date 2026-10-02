"""
Domain services for Patient Consents.

All mutations remain behind this service boundary.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.patient_management.consents.constants import (
    ConsentStatus,
)
from apps.patient_management.consents.exceptions import (
    ConsentAlreadyGrantedError,
    InvalidConsentStateError,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)


@transaction.atomic
def create_consent(
    *,
    validated_data: Mapping[str, Any],
    performed_by,
) -> PatientConsent:
    """
    Create a Patient Consent.
    """
    data = dict(validated_data)
    data["created_by"] = performed_by

    return PatientConsent.objects.create(
        **data,
    )


@transaction.atomic
def update_consent(
    *,
    instance: PatientConsent,
    validated_data: Mapping[str, Any],
    performed_by,
) -> PatientConsent:
    """
    Update mutable Patient Consent fields.
    """
    protected = {
        "id",
        "organization",
        "organization_id",
        "patient",
        "patient_id",
        "created_at",
        "created_by",
        "created_by_id",
        "granted_by",
        "granted_at",
        "revoked_at",
        "status",
        "is_deleted",
        "deleted_at",
        "deleted_by_id",
    }

    changes = {
        key: value
        for key, value in dict(validated_data).items()
        if key not in protected
    }

    for field, value in changes.items():
        setattr(
            instance,
            field,
            value,
        )

    if changes:
        instance.save(
            update_fields=[
                *changes.keys(),
                "updated_at",
            ],
        )

    return instance


@transaction.atomic
def delete_consent(
    *,
    instance: PatientConsent,
    performed_by,
) -> PatientConsent:
    """
    Soft-delete a Patient Consent.
    """
    instance.is_deleted = True
    instance.is_active = False
    instance.deleted_at = timezone.now()
    instance.deleted_by_id = performed_by.pk
    instance.save(
        update_fields=[
            "is_deleted",
            "is_active",
            "deleted_at",
            "deleted_by_id",
            "updated_at",
        ],
    )
    return instance


@transaction.atomic
def restore_consent(
    *,
    instance: PatientConsent,
    performed_by,
) -> PatientConsent:
    """
    Restore a previously deleted Patient Consent.
    """
    instance.is_deleted = False
    instance.is_active = True
    instance.deleted_at = None
    instance.deleted_by_id = None
    instance.save(
        update_fields=[
            "is_deleted",
            "is_active",
            "deleted_at",
            "deleted_by_id",
            "updated_at",
        ],
    )
    return instance


@transaction.atomic
def grant_consent(
    *,
    instance: PatientConsent,
    performed_by,
) -> PatientConsent:
    """
    Grant a pending Patient Consent.
    """
    if instance.status == ConsentStatus.GRANTED:
        raise ConsentAlreadyGrantedError(
            "Patient consent is already granted.",
        )

    if instance.status in {
        ConsentStatus.REVOKED,
        ConsentStatus.EXPIRED,
    }:
        raise InvalidConsentStateError(
            "A revoked or expired consent cannot be granted again.",
        )

    instance.status = ConsentStatus.GRANTED
    instance.granted_at = timezone.now()
    instance.revoked_at = None
    instance.granted_by = performed_by
    instance.save(
        update_fields=[
            "status",
            "granted_at",
            "revoked_at",
            "granted_by",
            "updated_at",
        ],
    )
    return instance


@transaction.atomic
def revoke_consent(
    *,
    instance: PatientConsent,
    performed_by,
) -> PatientConsent:
    """
    Revoke a granted Patient Consent.
    """
    if instance.status != ConsentStatus.GRANTED:
        raise InvalidConsentStateError(
            "Only a granted consent can be revoked.",
        )

    instance.status = ConsentStatus.REVOKED
    instance.revoked_at = timezone.now()
    instance.is_active = False
    instance.save(
        update_fields=[
            "status",
            "revoked_at",
            "is_active",
            "updated_at",
        ],
    )
    return instance


__all__ = (
    "create_consent",
    "delete_consent",
    "grant_consent",
    "restore_consent",
    "revoke_consent",
    "update_consent",
)
