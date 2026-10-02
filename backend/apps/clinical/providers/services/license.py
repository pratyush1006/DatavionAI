"""
Provider license services.

Handles regulatory license
lifecycle operations.

Responsibilities:

- Create licenses
- Update licenses
- Verify licenses
- Suspend licenses
- Revoke licenses
- Expire licenses

Workflow layer controls
business orchestration.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.clinical.providers.constants import (
    LicenseStatus,
)
from apps.clinical.providers.models import (
    Provider,
    ProviderLicense,
)


class ProviderLicenseService:
    """
    Domain service for provider licenses.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        provider: Provider,
        validated_data: Mapping[str, Any],
    ) -> ProviderLicense:
        """
        Create provider license.
        """

        license = ProviderLicense(
            provider=provider,
            **validated_data,
        )

        license.full_clean()

        license.save()

        return license

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: ProviderLicense,
        validated_data: Mapping[str, Any],
    ) -> ProviderLicense:
        """
        Update provider license.
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
        instance: ProviderLicense,
    ) -> ProviderLicense:
        """
        Verify provider license.
        """

        instance.status = LicenseStatus.VERIFIED

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
    def suspend(
        *,
        instance: ProviderLicense,
    ) -> ProviderLicense:
        """
        Suspend provider license.
        """

        instance.status = LicenseStatus.SUSPENDED

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
    def revoke(
        *,
        instance: ProviderLicense,
    ) -> ProviderLicense:
        """
        Revoke provider license.
        """

        instance.status = LicenseStatus.REVOKED

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
    def expire(
        *,
        instance: ProviderLicense,
    ) -> ProviderLicense:
        """
        Mark license expired.
        """

        instance.status = LicenseStatus.EXPIRED

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
        instance: ProviderLicense,
    ) -> None:
        """
        Delete provider license.
        """

        instance.delete()


# Backward-compatible aliases

create_provider_license = ProviderLicenseService.create

update_provider_license = ProviderLicenseService.update

delete_provider_license = ProviderLicenseService.delete


__all__ = [
    "ProviderLicenseService",
    "create_provider_license",
    "update_provider_license",
    "delete_provider_license",
]
