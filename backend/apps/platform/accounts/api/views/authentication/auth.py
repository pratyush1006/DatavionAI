"""
Authentication API views.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    created_response,
    success_response,
)
from apps.common.http import (
    get_client_device,
    get_client_ip,
    get_client_location,
)
from apps.platform.accounts.api.serializers.authentication import (
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    RegisterSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Register User",
    description="Register a new user account.",
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
    },
)
class RegisterAPIView(APIView):
    """
    Register a new user.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = RegisterSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Register a new user.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        return created_response(
            message="Registration successful.",
            data={
                "id": str(user.id),
                "email": user.email,
                "is_verified": user.is_verified,
            },
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Login",
    description="Authenticate a user and return JWT tokens.",
    request=LoginSerializer,
    responses={
        200: LoginSerializer,
    },
)
class LoginAPIView(APIView):
    """
    Authenticate a user.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = LoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Authenticate a user.
        """

        serializer = self.serializer_class(
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

        tokens = serializer.save()

        return success_response(
            message="Login successful.",
            data=tokens,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Change Password",
    description="Change the authenticated user's password.",
    request=ChangePasswordSerializer,
    responses={
        200: None,
    },
)
class ChangePasswordAPIView(APIView):
    """
    Change the authenticated user's password.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = ChangePasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Change the authenticated user's password.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save(
            user=request.user,
        )

        return success_response(
            message="Password changed successfully.",
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Logout",
    description="Blacklist the supplied refresh token and logout the authenticated user.",
    request=LogoutSerializer,
    responses={
        200: None,
    },
)
class LogoutAPIView(APIView):
    """
    Logout the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = LogoutSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Logout the authenticated user.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Logout successful.",
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Refresh Token",
    description="Generate a new access token.",
    request=RefreshSerializer,
    responses={
        200: RefreshSerializer,
    },
)
class RefreshAPIView(APIView):
    """
    Refresh a JWT access token.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = RefreshSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Refresh an access token.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
        )


__all__ = [
    "ChangePasswordAPIView",
    "LoginAPIView",
    "LogoutAPIView",
    "RefreshAPIView",
    "RegisterAPIView",
]
