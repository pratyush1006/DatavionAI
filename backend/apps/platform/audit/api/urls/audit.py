"""
Audit API routes.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.audit.api.views import (
    AuditDetailAPIView,
    AuditListAPIView,
)

urlpatterns = [
    path(
        "",
        AuditListAPIView.as_view(),
        name="list",
    ),
    path(
        "<uuid:audit_log_id>/",
        AuditDetailAPIView.as_view(),
        name="detail",
    ),
]
