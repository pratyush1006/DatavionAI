"""
TaxRate services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.tax_gst.models import TaxRate


class TaxRateService:
    """
    Application service for tax_rate write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> TaxRate:
        """
        Create a new tax_rate.
        """

        instance = TaxRate(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: TaxRate,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> TaxRate:
        """
        Update an existing tax_rate.
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
        instance: TaxRate,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a tax_rate.
        """

        instance.hard_delete()


create_tax_rate = TaxRateService.create

update_tax_rate = TaxRateService.update

delete_tax_rate = TaxRateService.delete


__all__ = [
    "TaxRateService",
    "create_tax_rate",
    "update_tax_rate",
    "delete_tax_rate",
]
