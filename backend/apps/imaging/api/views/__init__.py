"""
Imaging API views initialization.
"""

from __future__ import annotations

from .ai_analysis import (
    AIAnalysisDetailAPIView,
    AIAnalysisListCreateAPIView,
    StudyAIAnalysisAPIView,
)
from .report import (
    ReportDetailAPIView,
    ReportListAPIView,
    StudyReportAPIView,
)
from .study import (
    StudyBulkCreateAPIView,
    StudyDetailAPIView,
    StudyListCreateAPIView,
)

__all__ = [
    "AIAnalysisDetailAPIView",
    "AIAnalysisListCreateAPIView",
    "ReportDetailAPIView",
    "ReportListAPIView",
    "StudyBulkCreateAPIView",
    "StudyDetailAPIView",
    "StudyListCreateAPIView",
    "StudyReportAPIView",
    "StudyAIAnalysisAPIView",
]
