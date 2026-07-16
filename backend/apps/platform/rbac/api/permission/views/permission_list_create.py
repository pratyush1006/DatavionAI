"""
API view for listing and creating permissions.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.permission.serializers import (
    PermissionCreateSerializer,
    PermissionDetailSerializer,
    PermissionListSerializer,
)
from apps.platform.rbac.models import (
    Permission,
)
from apps.platform.rbac.permissions import (
    CanCreatePermission,
    CanViewPermission,
)
from apps.platform.rbac.selectors import (
    get_permissions,
)
from apps.platform.rbac.services import (
    create_permission,
)
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

PERMISSION_TAG: Final = ("Permissions",)


@extend_schema(
    tags=[PERMISSION_TAG],
)
class PermissionListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing permissions or create a new permission.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPermission,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePermission,
        ),
    }

    serializer_classes = {
        "GET": PermissionListSerializer,
        "POST": PermissionCreateSerializer,
    }

    detail_serializer_class = PermissionDetailSerializer

    create_service = staticmethod(
        create_permission,
    )

    create_success_message = "Permission created successfully."

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "module",
        "action",
        "scope",
        "display_order",
    )

    ordering_fields = (
        "name",
        "module",
        "action",
        "scope",
        "display_order",
        "created_at",
    )

    filterset_fields = (
        "module",
        "action",
        "scope",
        "is_system",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Permission]:
        """
        Return the permissions queryset.
        """

        return get_permissions()


__all__ = [
    "PermissionListCreateAPIView",
]
