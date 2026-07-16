"""
User role list/create API view.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.user_role.serializers import (
    UserRoleCreateSerializer,
    UserRoleListSerializer,
)
from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.permissions import (
    CanCreateUserRole,
    CanViewUserRole,
)
from apps.platform.rbac.selectors import (
    get_user_roles,
)
from apps.platform.rbac.services import (
    create_user_role,
)
from drf_spectacular.utils import (
    extend_schema,
)


@extend_schema(
    tags=[
        "RBAC - User Roles",
    ],
)
class UserRoleListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    API view for listing and creating user roles.
    """

    queryset = UserRole.objects.none()

    create_service = staticmethod(create_user_role)

    def get_queryset(
        self,
    ):
        """
        Return the user role queryset.
        """

        return get_user_roles()

    def get_serializer_class(
        self,
    ):
        """
        Return the serializer class.
        """

        if self.request.method == "POST":
            return UserRoleCreateSerializer

        return UserRoleListSerializer

    def get_permissions(
        self,
    ):
        """
        Return permission instances.
        """

        if self.request.method == "POST":
            permission_classes = [
                CanCreateUserRole,
            ]
        else:
            permission_classes = [
                CanViewUserRole,
            ]

        return [permission() for permission in permission_classes]


__all__ = [
    "UserRoleListCreateAPIView",
]
