"""
API view for listing and creating users.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.accounts.api.serializers import (
    UserCreateSerializer,
    UserListSerializer,
)
from apps.accounts.models import User
from apps.accounts.permissions import (
    CanCreateUser,
    CanViewUser,
)
from apps.accounts.selectors.account import get_users
from apps.accounts.services import create_user
from apps.common.api.base_generics import BaseListCreateAPIView

ACCOUNT_TAG: Final = ("Accounts",)


@extend_schema(
    tags=ACCOUNT_TAG,
)
class UserListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing users or create a new user.
    """

    list_serializer_class = UserListSerializer

    create_serializer_class = UserCreateSerializer

    create_service = create_user

    permission_map = {
        "GET": (
            IsAuthenticated,
            CanViewUser,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateUser,
        ),
    }

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
        Return users queryset.
        """

        return get_users()
