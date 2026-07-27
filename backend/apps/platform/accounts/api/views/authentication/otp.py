"""
OTP authentication API views.

Handles:

- Email verification OTP
- OTP resend workflow
- Future login/password OTP flows

OTP lifecycle is delegated to services.
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
)
from apps.platform.accounts.api.serializers.authentication import (
    ResendOTPSerializer,
    VerifyOTPSerializer,
)

AUTH_TAG: Final = ("Authentication",)


class BaseOTPAPIView(
    BaseGenericAPIView,
):
    """
    Base OTP API.

    Provides common security context.
    """

    permission_classes = (AllowAny,)

    authentication_classes = ()

    def get_security_context(
        self,
        request: Request,
    ) -> dict[str, str]:
        """
        Extract request security metadata.
        """

        return {
            "ip_address": get_client_ip(
                request,
            ),
            "device": get_client_device(
                request,
            ),
        }


@extend_schema(
    tags=AUTH_TAG,
    summary="Verify Email OTP",
    description=("Verify a user's email address using OTP."),
    request=VerifyOTPSerializer,
    responses={
        200: None,
    },
)
class VerifyOTPAPIView(
    BaseOTPAPIView,
):
    """
    Verify email using OTP.
    """

    serializer_class = VerifyOTPSerializer

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
                **self.get_security_context(
                    request,
                ),
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return self.success_response(
            message=("Email verified successfully."),
            data=None,
        )


@extend_schema(
    tags=AUTH_TAG,
    summary="Resend Verification OTP",
    description=("Generate and resend email verification OTP."),
    request=ResendOTPSerializer,
    responses={
        200: None,
    },
)
class ResendOTPAPIView(
    BaseOTPAPIView,
):
    """
    Resend email verification OTP.
    """

    serializer_class = ResendOTPSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Resend OTP.
        """

        serializer = self.get_serializer(
            data=request.data,
            context={
                **self.get_security_context(
                    request,
                ),
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return self.success_response(
            message=("Verification OTP sent successfully."),
            data=None,
        )


__all__ = (
    "ResendOTPAPIView",
    "VerifyOTPAPIView",
)
