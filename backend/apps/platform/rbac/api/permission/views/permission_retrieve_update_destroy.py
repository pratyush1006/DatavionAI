"""
API view for retrieving, updating and deleting permissions.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.permission.serializers import (
    PermissionCreateSerializer,
    PermissionDetailSerializer,
)
from apps.platform.rbac.models import Permission
from apps.platform.rbac.permissions import (
    CanDeletePermission,
    CanUpdatePermission,
    CanViewPermission,
)
from apps.platform.rbac.selectors import (
    get_permission_by_id,
)
from apps.platform.rbac.services import (
    delete_permission,
    update_permission,
)

PERMISSION_TAG: Final = ("Permissions",)


@extend_schema(
    tags=[PERMISSION_TAG],
)
class PermissionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a permission.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPermission,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePermission,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePermission,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePermission,
        ),
    }

    serializer_classes = {
        "GET": PermissionDetailSerializer,
        "PUT": PermissionCreateSerializer,
        "PATCH": PermissionCreateSerializer,
    }
    queryset = Permission.objects.all()

    lookup_url_kwarg = "permission_id"

    detail_selector = staticmethod(
        get_permission_by_id,
    )

    update_service = staticmethod(
        update_permission,
    )

    delete_service = staticmethod(
        delete_permission,
    )

    update_success_message = "Permission updated successfully."

    delete_success_message = "Permission deleted successfully."


__all__ = [
    "PermissionRetrieveUpdateDestroyAPIView",
]
