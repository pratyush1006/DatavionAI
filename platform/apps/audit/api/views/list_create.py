"""
List view for the Audit application.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

from apps.audit.api.serializers import AuditListSerializer
from apps.audit.permissions import CanViewAudit
from apps.audit.selectors import get_audit_logs
from apps.common.api.base_generics import BaseListCreateAPIView


class AuditListAPIView(BaseListCreateAPIView):
    """
    GET -> List Audit Logs
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "module",
        "object_type",
        "object_id",
        "user__email",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "created_at",
        "action",
        "module",
    )

    filterset_fields = (
        "action",
        "module",
        "organization",
        "user",
    )

    permission_map = {
        "GET": (
            IsAuthenticated,
            CanViewAudit,
        ),
    }

    def get_permissions(self) -> list[BasePermission]:
        permission_classes = self.permission_map.get(
            self.request.method,
            (),
        )

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_audit_logs()

    def get_serializer_class(self):
        return AuditListSerializer

    @extend_schema(tags=["Audit"])
    def get(self, request, *args, **kwargs):
        return self.list(
            request,
            *args,
            **kwargs,
        )
