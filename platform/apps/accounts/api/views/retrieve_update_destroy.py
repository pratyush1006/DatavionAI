"""
API view for retrieving, updating and deleting users.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.accounts.api.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
)
from apps.accounts.selectors import get_user_by_id
from apps.accounts.services import (
    delete_user,
    update_user,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)


@extend_schema(tags=["Accounts"])
class UserRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete users.
    """

    permission_classes = (IsAuthenticated,)

    lookup_url_kwarg = "user_id"

    def get_object(self):
        """
        Return the requested user.
        """
        return get_user_by_id(
            user_id=self.kwargs["user_id"],
        )

    def get_serializer_class(self):
        """
        Return the appropriate serializer.
        """
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer

        return UserDetailSerializer

    def perform_update(
        self,
        serializer: UserUpdateSerializer,
    ) -> None:
        """
        Update the user.
        """
        self.instance = update_user(
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(
        self,
        instance,
    ) -> None:
        """
        Delete the user.
        """
        delete_user(
            instance=instance,
        )
