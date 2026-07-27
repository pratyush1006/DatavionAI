"""
API view for listing and creating users.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.common.permissions import (
    IsAuthenticatedAndActive,
)
from apps.platform.accounts.api.serializers import (
    UserCreateSerializer,
    UserListSerializer,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.accounts.permissions import (
    CanCreateUser,
    CanViewUser,
)
from apps.platform.accounts.selectors import (
    get_users,
)
from apps.platform.accounts.services import (
    UserService,
)

ACCOUNT_TAG: Final = ("Accounts",)


@extend_schema(
    tags=ACCOUNT_TAG,
)
class UserListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List users or create a user.
    """

    serializer_class = UserListSerializer

    serializer_classes = {
        "GET": UserListSerializer,
        "POST": UserCreateSerializer,
    }

    permission_classes_map = {
        "GET": (
            IsAuthenticatedAndActive,
            CanViewUser,
        ),
        "POST": (
            IsAuthenticatedAndActive,
            CanCreateUser,
        ),
    }

    create_service = UserService.create

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("email",)

    ordering_fields = (
        "email",
        "created_at",
    )

    def get_queryset(
        self,
    ) -> QuerySet[User]:
        """
        Return users scoped to current tenant.
        """

        return get_users(
            tenant=self.current_tenant,
        )


__all__ = ("UserListCreateAPIView",)
