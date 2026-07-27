"""
API view for retrieving, updating, and deactivating users.
"""

from __future__ import annotations

from typing import Final
from uuid import UUID

from drf_spectacular.utils import extend_schema

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.permissions import (
    IsAuthenticatedAndActive,
)
from apps.platform.accounts.api.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.accounts.permissions import (
    CanDeleteUser,
    CanUpdateUser,
    CanViewUser,
)
from apps.platform.accounts.selectors import (
    get_user_by_id,
)
from apps.platform.accounts.services import (
    UserService,
)

ACCOUNT_TAG: Final = ("Accounts",)


@extend_schema(
    tags=ACCOUNT_TAG,
)
class UserRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or deactivate a user.
    """

    lookup_url_kwarg = "user_id"

    serializer_class = UserDetailSerializer

    serializer_classes = {
        "GET": UserDetailSerializer,
        "PUT": UserUpdateSerializer,
        "PATCH": UserUpdateSerializer,
    }

    permission_classes_map = {
        "GET": (
            IsAuthenticatedAndActive,
            CanViewUser,
        ),
        "PUT": (
            IsAuthenticatedAndActive,
            CanUpdateUser,
        ),
        "PATCH": (
            IsAuthenticatedAndActive,
            CanUpdateUser,
        ),
        "DELETE": (
            IsAuthenticatedAndActive,
            CanDeleteUser,
        ),
    }

    update_service = UserService.update

    #
    # Healthcare SaaS rule:
    #
    # Never hard delete users.
    # Preserve audit history.
    #
    delete_service = UserService.deactivate

    def get_object(
        self,
    ) -> User:
        """
        Return tenant-scoped user
        with object permission validation.
        """

        user_id = UUID(
            str(
                self.kwargs[self.lookup_url_kwarg],
            ),
        )

        user = get_user_by_id(
            user_id=user_id,
            tenant=self.current_tenant,
        )

        if user is None:
            self.raise_not_found()

        self.check_object_permissions(
            user,
        )

        return user


__all__ = ("UserRetrieveUpdateDestroyAPIView",)
