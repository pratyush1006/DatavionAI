"""
Vendor services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.billing.accounts_payable.models import Vendor
from django.db import transaction


class VendorService:
    """
    Application service for vendor write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Vendor:
        """
        Create a new vendor.
        """

        instance = Vendor(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Vendor,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Vendor:
        """
        Update an existing vendor.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Vendor,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a vendor.
        """

        instance.hard_delete()


create_vendor = VendorService.create

update_vendor = VendorService.update

delete_vendor = VendorService.delete


__all__ = [
    "VendorService",
    "create_vendor",
    "update_vendor",
    "delete_vendor",
]
