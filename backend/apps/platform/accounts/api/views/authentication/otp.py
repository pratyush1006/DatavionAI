"""
OTP verification API views.
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
    ResendOTPSerializer,
    VerifyOTPSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Verify Email",
    description="Verify a user's email address using a one-time password.",
    request=VerifyOTPSerializer,
    responses={
        200: None,
    },
)
class VerifyOTPAPIView(APIView):
    """
    Verify a user's email address using an OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = VerifyOTPSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Verify the supplied OTP.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Email verified successfully.",
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Resend Verification OTP",
    description="Resend the email verification OTP.",
    request=ResendOTPSerializer,
    responses={
        200: None,
    },
)
class ResendOTPAPIView(APIView):
    """
    Resend an email verification OTP.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    serializer_class = ResendOTPSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Resend the verification OTP.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return success_response(
            message="Verification OTP sent successfully.",
            data=None,
        )


__all__ = [
    "ResendOTPAPIView",
    "VerifyOTPAPIView",
]
