"""
List/Create API for PermissionGroup.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.permission_group.serializers import (
    PermissionGroupCreateSerializer,
    PermissionGroupListSerializer,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.permissions import (
    CanCreatePermissionGroup,
    CanViewPermissionGroup,
)
from apps.platform.rbac.services import (
    create_permission_group,
)
from rest_framework.permissions import IsAuthenticated


class PermissionGroupListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create permission groups.
    """

    queryset = PermissionGroup.objects.active().ordered()

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPermissionGroup,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePermissionGroup,
        ),
    }

    serializer_classes = {
        "GET": PermissionGroupListSerializer,
        "POST": PermissionGroupCreateSerializer,
    }

    create_service = staticmethod(
        create_permission_group,
    )


__all__ = [
    "PermissionGroupListCreateAPIView",
]
