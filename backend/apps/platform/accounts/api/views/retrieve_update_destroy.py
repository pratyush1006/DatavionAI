"""
API view for retrieving, updating, and deleting users.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.accounts.api.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
)
from apps.platform.accounts.models import User
from apps.platform.accounts.permissions import (
    CanDeleteUser,
    CanUpdateUser,
    CanViewUser,
)
from apps.platform.accounts.selectors import get_user_by_id
from apps.platform.accounts.services import UserService

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

    #
    # Default serializer used by DRF,
    # Browsable API and drf-spectacular.
    #
    serializer_class = UserDetailSerializer

    #
    # HTTP method specific serializers.
    #
    serializer_classes = {
        "GET": UserDetailSerializer,
        "PUT": UserUpdateSerializer,
        "PATCH": UserUpdateSerializer,
    }

    #
    # HTTP method specific permissions.
    #
    permission_classes_map = {
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

    #
    # Services used by update/delete requests.
    #
    update_service = UserService.update

    delete_service = UserService.delete

    def get_object(
        self,
    ) -> User:
        """
        Return the requested user.
        """

        user = get_user_by_id(
            user_id=self.kwargs[self.lookup_url_kwarg],
        )

        if user is None:
            self.raise_not_found()

        return user


__all__ = [
    "UserRetrieveUpdateDestroyAPIView",
]
