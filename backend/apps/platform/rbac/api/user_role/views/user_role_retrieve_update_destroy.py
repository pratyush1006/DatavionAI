"""
User role retrieve/update/destroy API view.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.user_role.serializers import (
    UserRoleDetailSerializer,
    UserRoleUpdateSerializer,
)
from apps.platform.rbac.models import (
    UserRole,
)
from apps.platform.rbac.permissions import (
    CanDeleteUserRole,
    CanUpdateUserRole,
    CanViewUserRole,
)
from apps.platform.rbac.selectors import (
    get_user_role_by_id,
)
from apps.platform.rbac.services import (
    delete_user_role,
    update_user_role,
)
from drf_spectacular.utils import (
    extend_schema,
)


@extend_schema(
    tags=[
        "RBAC - User Roles",
    ],
)
class UserRoleRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    API view for retrieving, updating, and deleting a user role.
    """

    queryset = UserRole.objects.none()

    lookup_field = "id"

    update_service = staticmethod(update_user_role)

    delete_service = staticmethod(delete_user_role)

    def get_object(
        self,
    ) -> UserRole:
        """
        Return the requested user role.
        """

        return get_user_role_by_id(
            user_role_id=self.kwargs[self.lookup_field],
        )

    def get_serializer_class(
        self,
    ):
        """
        Return the serializer class.
        """

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return UserRoleUpdateSerializer

        return UserRoleDetailSerializer

    def get_permissions(
        self,
    ):
        """
        Return permission instances.
        """

        permission_map = {
            "GET": [
                CanViewUserRole,
            ],
            "PUT": [
                CanUpdateUserRole,
            ],
            "PATCH": [
                CanUpdateUserRole,
            ],
            "DELETE": [
                CanDeleteUserRole,
            ],
        }

        permission_classes = permission_map.get(
            self.request.method,
            [],
        )

        return [permission() for permission in permission_classes]


__all__ = [
    "UserRoleRetrieveUpdateDestroyAPIView",
]
