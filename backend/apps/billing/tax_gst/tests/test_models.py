"""
Tests for the Tax Gst models.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import (
    TaxFiling,
    TaxRate,
)
from apps.common.tests.base import BaseTestCase


class TaxRateModelTestCase(BaseTestCase):
    """
    Test cases for the TaxRate model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.instance = TaxRate.objects.create(
            organization=self.organization,
            code="GST18",
            name="GST 18%",
            rate="18.00",
        )

    def test_tax_rate_creation(
        self,
    ) -> None:
        """
        TaxRate should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.name,
            "GST 18%",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the tax_rate display string.
        """

        self.assertIn(
            "GST 18%",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        TaxRate model should use the configured database table.
        """

        self.assertEqual(
            TaxRate._meta.db_table,
            "tax_gst_tax_rates",
        )


class TaxFilingModelTestCase(BaseTestCase):
    """
    Test cases for the TaxFiling model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()
        self.tax_rate = TaxRate.objects.create(
            organization=self.organization,
            code="GST18",
            name="GST 18%",
            rate="18.00",
        )

        self.instance = TaxFiling.objects.create(
            organization=self.organization,
            period="2025-Q1",
            tax_rate=self.tax_rate,
        )

    def test_tax_filing_creation(
        self,
    ) -> None:
        """
        TaxFiling should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.period,
            "2025-Q1",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the tax_filing display string.
        """

        self.assertIn(
            "2025-Q1",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        TaxFiling model should use the configured database table.
        """

        self.assertEqual(
            TaxFiling._meta.db_table,
            "tax_gst_tax_filings",
        )


__all__ = [
    "TaxRateModelTestCase",
    "TaxFilingModelTestCase",
]
