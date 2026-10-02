"""
Retrieve/Update/Delete API for PermissionGroup.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.permission_group.serializers import (
    PermissionGroupDetailSerializer,
    PermissionGroupUpdateSerializer,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)
from apps.platform.rbac.permissions import (
    CanDeletePermissionGroup,
    CanUpdatePermissionGroup,
    CanViewPermissionGroup,
)
from apps.platform.rbac.selectors import (
    get_permission_group_by_id,
)
from apps.platform.rbac.services import (
    delete_permission_group,
    update_permission_group,
)


class PermissionGroupRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete permission groups.
    """

    queryset = PermissionGroup.objects.all()

    lookup_url_kwarg = "uuid"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPermissionGroup,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePermissionGroup,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePermissionGroup,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePermissionGroup,
        ),
    }

    serializer_classes = {
        "GET": PermissionGroupDetailSerializer,
        "PUT": PermissionGroupUpdateSerializer,
        "PATCH": PermissionGroupUpdateSerializer,
    }

    detail_selector = staticmethod(
        get_permission_group_by_id,
    )

    update_service = staticmethod(
        update_permission_group,
    )

    delete_service = staticmethod(
        delete_permission_group,
    )


__all__ = [
    "PermissionGroupRetrieveUpdateDestroyAPIView",
]
