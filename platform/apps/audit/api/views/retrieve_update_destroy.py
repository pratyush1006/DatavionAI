"""
Detail view for the Audit application.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

from apps.audit.api.serializers import AuditDetailSerializer
from apps.audit.permissions import CanViewAudit
from apps.audit.selectors import get_audit_log_by_id
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)


class AuditDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    GET -> Retrieve Audit Log
    """

    lookup_url_kwarg = "audit_log_id"

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

    def get_object(self):
        return get_audit_log_by_id(
            self.kwargs[self.lookup_url_kwarg],
        )

    def get_serializer_class(self):
        return AuditDetailSerializer

    @extend_schema(tags=["Audit"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )
