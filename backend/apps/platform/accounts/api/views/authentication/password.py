"""
Password management API views.
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

from apps.common.api.responses import success_response
from apps.platform.accounts.api.serializers.authentication import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Forgot Password",
    description="Generate and email a password reset OTP.",
    request=ForgotPasswordSerializer,
    responses={
        200: None,
    },
)
class ForgotPasswordAPIView(APIView):
    """
    Generate a password reset OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = ForgotPasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Generate a password reset OTP.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Password reset OTP sent successfully.",
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Reset Password",
    description="Reset a user's password using the emailed OTP.",
    request=ResetPasswordSerializer,
    responses={
        200: None,
    },
)
class ResetPasswordAPIView(APIView):
    """
    Reset a user's password using an OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = ResetPasswordSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Reset password.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Password reset successfully.",
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
        Change password.
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
        )


__all__ = [
    "ChangePasswordAPIView",
    "ForgotPasswordAPIView",
    "ResetPasswordAPIView",
]
