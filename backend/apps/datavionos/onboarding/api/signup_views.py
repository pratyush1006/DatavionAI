from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.api.base_generics import BaseGenericAPIView
from apps.common.http import get_client_device, get_client_ip
from apps.datavionos.onboarding.api.serializers import (
    OrganizationPreflightSerializer,
)
from apps.datavionos.onboarding.api.signup_serializers import (
    SelfServiceSignupSerializer,
)
from apps.datavionos.onboarding.plan_catalog import (
    OrganizationOnboardingValidationError,
)
from apps.datavionos.onboarding.signup import (
    SelfServiceEmailConflictError,
    SelfServicePaymentRequiredError,
    SelfServiceSignupError,
    SelfServiceSignupService,
)


class SelfServiceSignupPreflightAPIView(BaseGenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @extend_schema(
        tags=("Organization Onboarding",),
        request=OrganizationPreflightSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = OrganizationPreflightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = SelfServiceSignupService.preflight(
                organization_data=serializer.validated_data,
                plan_id=serializer.validated_data.get("plan_id"),
                plan_code=serializer.validated_data.get("plan_code"),
            )
        except OrganizationOnboardingValidationError as exc:
            return Response(
                {
                    "success": False,
                    "code": "organization_profile_invalid",
                    "detail": str(exc),
                },
                status=400,
            )

        return self.success_response(
            message="Self-service signup preflight completed.",
            data=result,
        )


class SelfServiceSignupAPIView(BaseGenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @extend_schema(
        tags=("Organization Onboarding",),
        request=SelfServiceSignupSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = SelfServiceSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data["account"]
        organization = dict(serializer.validated_data["organization"])

        plan_id = organization.pop("plan_id", None)
        plan_code = organization.pop("plan_code", None)

        try:
            result = SelfServiceSignupService.signup(
                account_data=account,
                organization_data=organization,
                plan_id=plan_id,
                plan_code=plan_code,
                ip_address=get_client_ip(request),
                user_agent=get_client_device(request),
            )
        except OrganizationOnboardingValidationError as exc:
            return Response(
                {
                    "success": False,
                    "code": "organization_profile_invalid",
                    "detail": str(exc),
                },
                status=400,
            )
        except SelfServicePaymentRequiredError as exc:
            return Response(
                {
                    "success": False,
                    "code": "payment_required",
                    "detail": str(exc),
                    "next_step": "payment",
                },
                status=402,
            )
        except SelfServiceEmailConflictError as exc:
            return Response(
                {
                    "success": False,
                    "code": "signup_conflict",
                    "detail": str(exc),
                    "next_step": "login",
                },
                status=409,
            )
        except SelfServiceSignupError as exc:
            return Response(
                {
                    "success": False,
                    "code": "signup_failed",
                    "detail": str(exc),
                },
                status=400,
            )

        return self.created_response(
            message="Organization signup completed. Please verify your email address.",
            data=result.as_dict(),
        )


__all__ = [
    "SelfServiceSignupAPIView",
    "SelfServiceSignupPreflightAPIView",
]
