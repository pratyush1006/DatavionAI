"""
OAuth authentication API views.

Handles:

- Google OAuth authentication
- Microsoft OAuth authentication
- OAuth security context tracking
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.http import (
    get_client_device,
    get_client_ip,
    get_client_location,
)
from apps.platform.accounts.api.serializers.authentication import (
    GoogleLoginSerializer,
    MicrosoftLoginSerializer,
    TokenResponseSerializer,
)

AUTH_TAG: Final = ("Authentication",)


class BaseOAuthLoginAPIView(
    BaseGenericAPIView,
):
    """
    Base OAuth login API.

    Adds security context before
    authentication.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    def perform_oauth_login(
        self,
        request: Request,
    ) -> dict[str, str]:
        """
        Execute OAuth authentication.
        """

        serializer = self.get_serializer(
            data=request.data,
            context={
                "ip_address": get_client_ip(
                    request,
                ),
                "device": get_client_device(
                    request,
                ),
                "location": get_client_location(
                    request,
                ),
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return serializer.save()


@extend_schema(
    tags=AUTH_TAG,
    summary="Google Login",
    description=("Authenticate using Google OAuth."),
    request=GoogleLoginSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class GoogleLoginAPIView(
    BaseOAuthLoginAPIView,
):
    """
    Authenticate using Google OAuth.
    """

    serializer_class = GoogleLoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate using Google.
        """

        tokens = self.perform_oauth_login(
            request,
        )

        return self.success_response(
            message=("Google authentication successful."),
            data=tokens,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Microsoft Login",
    description=("Authenticate using Microsoft OAuth."),
    request=MicrosoftLoginSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class MicrosoftLoginAPIView(
    BaseOAuthLoginAPIView,
):
    """
    Authenticate using Microsoft OAuth.
    """

    serializer_class = MicrosoftLoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate using Microsoft.
        """

        tokens = self.perform_oauth_login(
            request,
        )

        return self.success_response(
            message=("Microsoft authentication successful."),
            data=tokens,
        )


__all__ = (
    "GoogleLoginAPIView",
    "MicrosoftLoginAPIView",
)
