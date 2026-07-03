"""
API view for retrieving, updating, and deleting users.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.accounts.api.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
)
from apps.accounts.models import User
from apps.accounts.permissions import (
    CanDeleteUser,
    CanUpdateUser,
    CanViewUser,
)
from apps.accounts.selectors.account import get_user_by_id
from apps.accounts.services import (
    delete_user,
    update_user,
)
from apps.common.api.base_generics import BaseRetrieveUpdateDestroyAPIView

ACCOUNT_TAG: Final = ("Accounts",)


@extend_schema(
    tags=ACCOUNT_TAG,
)
class UserRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a user.
    """

    lookup_url_kwarg = "user_id"

    detail_serializer_class = UserDetailSerializer

    update_serializer_class = UserUpdateSerializer

    update_service = update_user

    delete_service = delete_user

    permission_map = {
        "GET": (
            IsAuthenticated,
            CanViewUser,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateUser,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateUser,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteUser,
        ),
    }

    def get_object(
        self,
    ) -> User:
        """
        Return the requested user.
        """

        return get_user_by_id(
            user_id=self.kwargs[self.lookup_url_kwarg],
        )
