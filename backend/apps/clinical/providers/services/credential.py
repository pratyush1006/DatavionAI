"""
Provider credential services.

Handles provider qualification
and credential lifecycle operations.

Responsibilities:

- Create credentials
- Update credentials
- Verify credentials
- Reject credentials
- Expire credentials

Workflow layer orchestrates
business processes.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.constants import (
    CredentialStatus,
)
from apps.clinical.providers.models import (
    Provider,
    ProviderCredential,
)


class ProviderCredentialService:
    """
    Domain service for provider credentials.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        provider: Provider,
        validated_data: Mapping[str, Any],
    ) -> ProviderCredential:
        """
        Create provider credential.
        """

        credential = ProviderCredential(
            provider=provider,
            **validated_data,
        )

        credential.full_clean()

        credential.save()

        return credential

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ProviderCredential,
        validated_data: Mapping[str, Any],
    ) -> ProviderCredential:
        """
        Update credential.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save(
            update_fields=[
                *validated_data.keys(),
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: ProviderCredential,
    ) -> ProviderCredential:
        """
        Verify credential.
        """

        instance.status = CredentialStatus.VERIFIED

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def reject(
        *,
        instance: ProviderCredential,
        remarks: str = "",
    ) -> ProviderCredential:
        """
        Reject credential.
        """

        instance.status = CredentialStatus.REJECTED

        if remarks:
            instance.remarks = remarks

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "remarks",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def expire(
        *,
        instance: ProviderCredential,
    ) -> ProviderCredential:
        """
        Mark credential expired.
        """

        instance.status = CredentialStatus.EXPIRED

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: ProviderCredential,
    ) -> None:
        """
        Delete credential.
        """

        instance.delete()


# Backward-compatible aliases

create_provider_credential = ProviderCredentialService.create

update_provider_credential = ProviderCredentialService.update

delete_provider_credential = ProviderCredentialService.delete


__all__ = [
    "ProviderCredentialService",
    "create_provider_credential",
    "update_provider_credential",
    "delete_provider_credential",
]
