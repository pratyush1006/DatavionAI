"""
Financial Management API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.financial_management.api.views import (
    BudgetListCreateAPIView,
    BudgetRetrieveUpdateDestroyAPIView,
    FinancialReportListCreateAPIView,
    FinancialReportRetrieveUpdateDestroyAPIView,
)

app_name = "financial_management"

urlpatterns = [
    path(
        "budgets/",
        BudgetListCreateAPIView.as_view(),
        name="budget-list-create",
    ),
    path(
        "budgets/<uuid:budget_id>/",
        BudgetRetrieveUpdateDestroyAPIView.as_view(),
        name="budget-detail",
    ),
    path(
        "financial_reports/",
        FinancialReportListCreateAPIView.as_view(),
        name="financial_report-list-create",
    ),
    path(
        "financial_reports/<uuid:financial_report_id>/",
        FinancialReportRetrieveUpdateDestroyAPIView.as_view(),
        name="financial_report-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
