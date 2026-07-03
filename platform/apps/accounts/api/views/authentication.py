"""
Authentication API views.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.api.serializers import (
    LoginSerializer,
    MeSerializer,
)
from apps.accounts.services import generate_tokens

AUTHENTICATION_TAG = ("Authentication",)


class LoginAPIView(APIView):
    """
    Authenticate a user and return JWT tokens.
    """

    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        tags=AUTHENTICATION_TAG,
        request=LoginSerializer,
        responses={200: MeSerializer},
    )
    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate the user and return access and refresh tokens.
        """

        serializer = LoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data["user"]

        tokens = generate_tokens(
            user=user,
        )

        return Response(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": MeSerializer(
                    user,
                ).data,
            },
            status=status.HTTP_200_OK,
        )


class MeAPIView(APIView):
    """
    Return details of the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=AUTHENTICATION_TAG,
        responses={200: MeSerializer},
    )
    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return the currently authenticated user.
        """

        return Response(
            MeSerializer(
                request.user,
            ).data,
            status=status.HTTP_200_OK,
        )


__all__ = [
    "LoginAPIView",
    "MeAPIView",
]
