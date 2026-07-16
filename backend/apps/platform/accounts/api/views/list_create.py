"""
API view for listing and creating users.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.platform.accounts.api.serializers import (
    UserCreateSerializer,
    UserListSerializer,
)
from apps.platform.accounts.models import User
from apps.platform.accounts.permissions import (
    CanCreateUser,
    CanViewUser,
)
from apps.platform.accounts.selectors import get_users
from apps.platform.accounts.services import UserService

ACCOUNT_TAG: Final = ("Accounts",)


@extend_schema(
    tags=ACCOUNT_TAG,
)
class UserListCreateAPIView(BaseListCreateAPIView):
    """
    List existing users or create a new user.
    """

    #
    # Default serializer used by DRF, Browsable API,
    # and drf-spectacular.
    #
    serializer_class = UserListSerializer

    #
    # HTTP method specific serializers.
    #
    serializer_classes = {
        "GET": UserListSerializer,
        "POST": UserCreateSerializer,
    }

    #
    # HTTP method specific permissions.
    #
    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewUser,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateUser,
        ),
    }

    #
    # Service used by POST requests.
    #
    create_service = UserService.create

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("email",)

    ordering_fields = (
        "username",
        "email",
        "created_at",
    )

    def get_queryset(
        self,
    ) -> QuerySet[User]:
        """
        Return the users queryset.
        """

        return get_users()


__all__ = [
    "UserListCreateAPIView",
]
