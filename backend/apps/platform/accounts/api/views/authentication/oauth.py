"""
OAuth authentication API views.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.platform.accounts.api.serializers.authentication import (
    GoogleLoginSerializer,
    MicrosoftLoginSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Google Login",
    description="Authenticate using Google OAuth.",
    request=GoogleLoginSerializer,
)
class GoogleLoginAPIView(APIView):
    """
    Authenticate using Google OAuth.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = GoogleLoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate using Google.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Google authentication completed.",
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Microsoft Login",
    description="Authenticate using Microsoft OAuth.",
    request=MicrosoftLoginSerializer,
)
class MicrosoftLoginAPIView(APIView):
    """
    Authenticate using Microsoft OAuth.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = MicrosoftLoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate using Microsoft.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Microsoft authentication completed.",
        )


__all__ = [
    "GoogleLoginAPIView",
    "MicrosoftLoginAPIView",
]
