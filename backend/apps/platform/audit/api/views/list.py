"""
List view for the Audit application.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.audit.api.serializers import (
    AuditListSerializer,
)
from apps.platform.audit.permissions import (
    CanViewAudit,
)
from apps.platform.audit.selectors import (
    get_audit_logs,
)


@extend_schema(
    tags=[
        "Audit",
    ],
)
class AuditListAPIView(
    BaseListCreateAPIView,
):
    """
    Read-only endpoint for listing audit logs.
    """

    serializer_class = AuditListSerializer

    http_method_names = [
        "get",
        "head",
        "options",
    ]

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
        "success",
    )

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAudit,
        ),
    }

    def get_queryset(
        self,
    ):
        """
        Return audit logs.
        """

        return get_audit_logs()


__all__ = [
    "AuditListAPIView",
]
