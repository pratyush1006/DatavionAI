"""
Imaging API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.imaging.api.views import (
    AIAnalysisDetailAPIView,
    AIAnalysisListCreateAPIView,
    ReportDetailAPIView,
    ReportListAPIView,
    StudyAIAnalysisAPIView,
    StudyBulkCreateAPIView,
    StudyDetailAPIView,
    StudyListCreateAPIView,
    StudyReportAPIView,
)

app_name = "imaging"

urlpatterns = [
    path(
        "studies/",
        StudyListCreateAPIView.as_view(),
        name="study-list-create",
    ),
    path(
        "studies/<uuid:study_id>/",
        StudyDetailAPIView.as_view(),
        name="study-detail",
    ),
    path(
        "studies/<uuid:study_id>/report/",
        StudyReportAPIView.as_view(),
        name="study-report",
    ),
    path(
        "studies/<uuid:study_id>/ai-analysis/",
        StudyAIAnalysisAPIView.as_view(),
        name="study-ai-analysis",
    ),
    path(
        "studies/bulk/",
        StudyBulkCreateAPIView.as_view(),
        name="study-bulk-create",
    ),
    path(
        "reports/",
        ReportListAPIView.as_view(),
        name="report-list",
    ),
    path(
        "reports/<uuid:report_id>/",
        ReportDetailAPIView.as_view(),
        name="report-detail",
    ),
    path(
        "ai-analysis/",
        AIAnalysisListCreateAPIView.as_view(),
        name="ai-analysis-list-create",
    ),
    path(
        "ai-analysis/<uuid:analysis_id>/",
        AIAnalysisDetailAPIView.as_view(),
        name="ai-analysis-detail",
    ),
]
