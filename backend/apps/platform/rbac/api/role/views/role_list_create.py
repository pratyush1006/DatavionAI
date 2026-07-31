"""
Role list/create API view.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.role.serializers import (
    RoleCreateSerializer,
    RoleListSerializer,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.permissions import (
    CanCreateRole,
    CanViewRole,
)
from apps.platform.rbac.selectors import (
    get_roles,
)
from apps.platform.rbac.services import (
    create_role,
)


@extend_schema(
    tags=[
        "RBAC - Roles",
    ],
)
class RoleListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    API view for listing and creating roles.
    """

    queryset = Role.objects.none()

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewRole,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateRole,
        ),
    }

    serializer_classes = {
        "GET": RoleListSerializer,
        "POST": RoleCreateSerializer,
    }

    list_selector = staticmethod(
        get_roles,
    )

    create_service = staticmethod(
        create_role,
    )


__all__ = [
    "RoleListCreateAPIView",
]
