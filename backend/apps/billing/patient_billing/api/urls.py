"""Patient Billing API URLs."""

from __future__ import annotations

from apps.billing.patient_billing.api.views import (
    PatientBillingAccountDetailAPIView,
    PatientBillingAccountListCreateAPIView,
    PatientBillingAccountTransitionAPIView,
    PatientBillingStatementGenerateAPIView,
    PatientBillingStatementIssueAPIView,
    PatientBillingStatementListAPIView,
    PatientBillingStatementVoidAPIView,
    PatientGuarantorDetailAPIView,
    PatientGuarantorListCreateAPIView,
    PatientGuarantorRestoreAPIView,
    PatientResponsibilityDetailAPIView,
    PatientResponsibilityListCreateAPIView,
    PatientResponsibilityRestoreAPIView,
)
from django.urls import path

app_name = "patient_billing"

urlpatterns = (
    path(
        "patient-accounts/",
        PatientBillingAccountListCreateAPIView.as_view(),
        name="patient-account-list-create",
    ),
    path(
        "patient-accounts/<uuid:pk>/",
        PatientBillingAccountDetailAPIView.as_view(),
        name="patient-account-detail",
    ),
    path(
        "patient-accounts/<uuid:pk>/transition/",
        PatientBillingAccountTransitionAPIView.as_view(),
        name="patient-account-transition",
    ),
    path(
        "patient-guarantors/",
        PatientGuarantorListCreateAPIView.as_view(),
        name="guarantor-list-create",
    ),
    path(
        "patient-guarantors/<uuid:pk>/",
        PatientGuarantorDetailAPIView.as_view(),
        name="guarantor-detail",
    ),
    path(
        "patient-guarantors/<uuid:pk>/restore/",
        PatientGuarantorRestoreAPIView.as_view(),
        name="guarantor-restore",
    ),
    path(
        "patient-accounts/<uuid:account_id>/responsibilities/",
        PatientResponsibilityListCreateAPIView.as_view(),
        name="responsibility-list-create",
    ),
    path(
        "patient-responsibilities/<uuid:pk>/",
        PatientResponsibilityDetailAPIView.as_view(),
        name="responsibility-detail",
    ),
    path(
        "patient-responsibilities/<uuid:pk>/restore/",
        PatientResponsibilityRestoreAPIView.as_view(),
        name="responsibility-restore",
    ),
    path(
        "patient-statements/",
        PatientBillingStatementListAPIView.as_view(),
        name="statement-list",
    ),
    path(
        "patient-statements/generate/",
        PatientBillingStatementGenerateAPIView.as_view(),
        name="statement-generate",
    ),
    path(
        "patient-statements/<uuid:pk>/issue/",
        PatientBillingStatementIssueAPIView.as_view(),
        name="statement-issue",
    ),
    path(
        "patient-statements/<uuid:pk>/void/",
        PatientBillingStatementVoidAPIView.as_view(),
        name="statement-void",
    ),
)

__all__ = (
    "app_name",
    "urlpatterns",
)
