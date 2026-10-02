"""
Password authentication API views.

Handles:

- Forgot password
- Reset password
- Change password

Business logic is delegated to PasswordService.
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
from apps.platform.accounts.api.serializers.authentication import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Forgot Password",
    description=(
        "Generate password reset OTP. "
        "For security reasons the response "
        "does not reveal whether an account exists."
    ),
    request=ForgotPasswordSerializer,
)
class ForgotPasswordAPIView(
    BaseGenericAPIView,
):
    """
    Request password reset OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = ForgotPasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Generate password reset OTP.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return self.success_response(
            message=("If the account exists, a password reset OTP has been sent."),
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Reset Password",
    description=("Reset password using OTP verification."),
    request=ResetPasswordSerializer,
)
class ResetPasswordAPIView(
    BaseGenericAPIView,
):
    """
    Reset password using OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = ResetPasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Reset user password.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return self.success_response(
            message=("Password reset successfully."),
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Change Password",
    description=("Change password for authenticated user."),
    request=ChangePasswordSerializer,
)
class ChangePasswordAPIView(
    BaseGenericAPIView,
):
    """
    Change authenticated user password.
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
            message=("Password changed successfully."),
            data=None,
        )


__all__ = (
    "ChangePasswordAPIView",
    "ForgotPasswordAPIView",
    "ResetPasswordAPIView",
)
