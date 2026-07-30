"""
TaxFiling services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.tax_gst.models import TaxFiling


class TaxFilingService:
    """
    Application service for tax_filing write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> TaxFiling:
        """
        Create a new tax_filing.
        """

        instance = TaxFiling(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: TaxFiling,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> TaxFiling:
        """
        Update an existing tax_filing.
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
        instance: TaxFiling,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a tax_filing.
        """

        instance.hard_delete()


create_tax_filing = TaxFilingService.create

update_tax_filing = TaxFilingService.update

delete_tax_filing = TaxFilingService.delete


__all__ = [
    "TaxFilingService",
    "create_tax_filing",
    "update_tax_filing",
    "delete_tax_filing",
]
