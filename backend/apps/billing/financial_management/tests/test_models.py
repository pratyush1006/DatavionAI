"""
Tests for the Financial Management models.
"""

from __future__ import annotations

from apps.billing.financial_management.models import (
    Budget,
    FinancialReport,
)
from apps.common.tests.base import BaseTestCase


class BudgetModelTestCase(BaseTestCase):
    """
    Test cases for the Budget model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.instance = Budget.objects.create(
            organization=self.organization,
            name="FY25 Ops",
            fiscal_year="FY2025",
            total_amount="100000.00",
        )

    def test_budget_creation(
        self,
    ) -> None:
        """
        Budget should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.name,
            "FY25 Ops",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the budget display string.
        """

        self.assertIn(
            "FY25 Ops",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        Budget model should use the configured database table.
        """

        self.assertEqual(
            Budget._meta.db_table,
            "financial_management_budgets",
        )


class FinancialReportModelTestCase(BaseTestCase):
    """
    Test cases for the FinancialReport model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()
        self.budget = Budget.objects.create(
            organization=self.organization,
            name="FY25 Ops",
            fiscal_year="FY2025",
            total_amount="100000.00",
        )

        self.instance = FinancialReport.objects.create(
            organization=self.organization,
            title="Q1 Report",
            report_type="balance_sheet",
            budget=self.budget,
        )

    def test_financial_report_creation(
        self,
    ) -> None:
        """
        FinancialReport should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.title,
            "Q1 Report",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the financial_report display string.
        """

        self.assertIn(
            "Q1 Report",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        FinancialReport model should use the configured database table.
        """

        self.assertEqual(
            FinancialReport._meta.db_table,
            "financial_management_financial_reports",
        )


__all__ = [
    "BudgetModelTestCase",
    "FinancialReportModelTestCase",
]
