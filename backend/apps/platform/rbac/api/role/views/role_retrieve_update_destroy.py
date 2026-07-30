"""
Role retrieve/update/destroy API view.
"""

from __future__ import annotations

from drf_spectacular.utils import (
    extend_schema,
)

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.role.serializers import (
    RoleDetailSerializer,
    RoleUpdateSerializer,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.permissions import (
    CanDeleteRole,
    CanUpdateRole,
    CanViewRole,
)
from apps.platform.rbac.selectors import (
    get_role_by_id,
)
from apps.platform.rbac.services import (
    delete_role,
    update_role,
)


@extend_schema(
    tags=[
        "RBAC - Roles",
    ],
)
class RoleRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    API view for retrieving, updating, and deleting a role.
    """

    queryset = Role.objects.none()

    lookup_field = "id"

    update_service = staticmethod(
        update_role,
    )

    delete_service = staticmethod(
        delete_role,
    )

    def get_object(
        self,
    ) -> Role:
        """
        Return the requested role.
        """

        return get_role_by_id(
            role_id=self.kwargs[self.lookup_field],
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
            return RoleUpdateSerializer

        return RoleDetailSerializer

    def get_permissions(
        self,
    ):
        """
        Return permission instances.
        """

        permission_map = {
            "GET": [
                CanViewRole,
            ],
            "PUT": [
                CanUpdateRole,
            ],
            "PATCH": [
                CanUpdateRole,
            ],
            "DELETE": [
                CanDeleteRole,
            ],
        }

        permission_classes = permission_map.get(
            self.request.method,
            [],
        )

        return [permission() for permission in permission_classes]


__all__ = [
    "RoleRetrieveUpdateDestroyAPIView",
]
