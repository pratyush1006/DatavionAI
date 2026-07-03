"""
API URLs for the Audit application.
"""

from __future__ import annotations

from django.urls import path

from apps.audit.api.views import (
    AuditDetailAPIView,
    AuditListAPIView,
)

urlpatterns = [
    path(
        "",
        AuditListAPIView.as_view(),
        name="audit-list",
    ),
    path(
        "<uuid:audit_log_id>/",
        AuditDetailAPIView.as_view(),
        name="audit-detail",
    ),
]
