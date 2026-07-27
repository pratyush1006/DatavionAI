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

from apps.common.api.base_generics import (
    BaseGenericAPIView,
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
    TokenResponseSerializer,
    VerifyLoginOTPSerializer,
)
from apps.platform.accounts.api.serializers.summary import (
    UserSummarySerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Register User",
    description="Register a new user account.",
    request=RegisterSerializer,
    responses={
        201: UserSummarySerializer,
    },
)
class RegisterAPIView(
    BaseGenericAPIView,
):
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
        Register user.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        response_serializer = UserSummarySerializer(
            user,
        )

        return self.created_response(
            message="Registration successful.",
            data=response_serializer.data,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Login",
    description=("Validate credentials and send login OTP."),
    request=LoginSerializer,
)
class LoginAPIView(
    BaseGenericAPIView,
):
    """
    Request login OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = LoginSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Generate login OTP.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        result = serializer.save()

        return self.success_response(
            message="Login OTP sent successfully.",
            data=result,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Verify Login OTP",
    description=("Verify login OTP and issue JWT tokens."),
    request=VerifyLoginOTPSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class VerifyLoginOTPAPIView(
    BaseGenericAPIView,
):
    """
    Verify login OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = VerifyLoginOTPSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Verify OTP.
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

        tokens = serializer.save(
            ip_address=serializer.context.get(
                "ip_address",
                "",
            ),
            device=serializer.context.get(
                "device",
                "Unknown Device",
            ),
            location=serializer.context.get(
                "location",
                "Unknown Location",
            ),
        )

        return self.success_response(
            message="Login successful.",
            data=tokens,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Change Password",
    description="Change authenticated user's password.",
    request=ChangePasswordSerializer,
)
class ChangePasswordAPIView(
    BaseGenericAPIView,
):
    """
    Change password.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = ChangePasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Change password.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save(
            user=request.user,
        )

        return self.success_response(
            message="Password changed successfully.",
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Logout",
    description=("Blacklist refresh token."),
    request=LogoutSerializer,
)
class LogoutAPIView(
    BaseGenericAPIView,
):
    """
    Logout user.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = LogoutSerializer

    def post(
        self,
        request: Request,
    ) -> Response:

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return self.success_response(
            message="Logout successful.",
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Refresh Token",
    description="Generate a new JWT access token.",
    request=RefreshSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class RefreshAPIView(
    BaseGenericAPIView,
):
    """
    Refresh JWT token.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = RefreshSerializer

    def post(
        self,
        request: Request,
    ) -> Response:

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return self.success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
        )


__all__ = (
    "ChangePasswordAPIView",
    "LoginAPIView",
    "LogoutAPIView",
    "RefreshAPIView",
    "RegisterAPIView",
    "VerifyLoginOTPAPIView",
)
