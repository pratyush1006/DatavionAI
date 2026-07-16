"""
Detail view for the Audit application.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.audit.api.serializers import (
    AuditDetailSerializer,
)
from apps.platform.audit.permissions import (
    CanViewAudit,
)
from apps.platform.audit.selectors import (
    get_audit_log_by_id,
)


@extend_schema(
    tags=[
        "Audit",
    ],
)
class AuditDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Read-only endpoint for retrieving
    a single audit log.
    """

    serializer_class = AuditDetailSerializer

    lookup_url_kwarg = "audit_log_id"

    #
    # Disable PUT/PATCH/DELETE while still
    # using the project's base generic view.
    #
    http_method_names = [
        "get",
        "head",
        "options",
    ]

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAudit,
        ),
    }

    def get_object(
        self,
    ):
        """
        Return the requested audit log.
        """

        return get_audit_log_by_id(
            self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "AuditDetailAPIView",
]
