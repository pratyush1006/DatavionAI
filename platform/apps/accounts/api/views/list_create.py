"""
API view for listing and creating users.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.accounts.api.serializers import (
    UserCreateSerializer,
    UserListSerializer,
)
from apps.accounts.selectors import get_users
from apps.accounts.services import create_user
from apps.common.api.base_generics import BaseListCreateAPIView


@extend_schema(tags=["Accounts"])
class UserListCreateAPIView(BaseListCreateAPIView):
    """
    List and create users.
    """

    serializer_class = UserListSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering_fields = (
        "username",
        "email",
        "created_at",
    )

    ordering = ("email",)

    def get_queryset(self):
        """
        Return the queryset for listing users.
        """
        return get_users()

    def get_serializer_class(self):
        """
        Return the appropriate serializer.
        """
        if self.request.method == "POST":
            return UserCreateSerializer

        return UserListSerializer

    def perform_create(
        self,
        serializer: UserCreateSerializer,
    ) -> None:
        """
        Create a new user.
        """
        self.instance = create_user(
            validated_data=serializer.validated_data,
        )

    def create(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Create a user and return the detail serializer.
        """
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_create(
            serializer,
        )

        output_serializer = UserListSerializer(
            self.instance,
            context=self.get_serializer_context(),
        )

        return self.created_response(
            data=output_serializer.data,
        )
