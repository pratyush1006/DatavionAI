from __future__ import annotations

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.datavionos.onboarding.api.serializers import (
    OrganizationOnboardingSerializer,
    OrganizationPreflightSerializer,
    OrganizationTypeSerializer,
    SaaSPlanSerializer,
)
from apps.datavionos.onboarding.contracts import OrganizationOnboardingRequest
from apps.datavionos.onboarding.plan_catalog import (
    OrganizationOnboardingValidationError,
    plan_is_eligible_for_onboarding,
)
from apps.datavionos.onboarding.registration import (
    OrganizationRegistrationError,
    OrganizationRegistrationOrchestrator,
)
from apps.platform.organizations.constants import (
    ORGANIZATION_CATEGORY_TYPES,
    OrganizationCategory,
    OrganizationType,
)
from apps.platform.organizations.models import Organization
from apps.platform.rbac.models import OrganizationRole
from apps.platform.saas_billing.models import Plan
from apps.platform.tenancy.models import TenantMembership


class OrganizationOnboardingContextMixin:
    """Resolve a trusted active tenant owned by the authenticated user."""

    def get_owner_tenant(self, request: Request):
        membership = (
            TenantMembership.objects.filter(
                user=request.user,
                status=TenantMembership.Status.ACTIVE,
                is_owner=True,
            )
            .select_related("tenant")
            .first()
        )

        if membership is None:
            raise PermissionError("An active tenant-owner membership is required.")

        return membership.tenant


@extend_schema(
    tags=("Organization Onboarding",),
    responses=OrganizationTypeSerializer(many=True),
)
class OrganizationTypeListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(
        self,
        request: Request,
    ) -> Response:
        data = []

        for choice in OrganizationType:
            category = next(
                (
                    category_choice.value
                    for category_choice, valid_types in ORGANIZATION_CATEGORY_TYPES.items()
                    if choice.value in {item.value for item in valid_types}
                ),
                "",
            )

            category_label = next(
                (
                    str(category_choice.label)
                    for category_choice in OrganizationCategory
                    if category_choice.value == category
                ),
                category,
            )

            data.append(
                {
                    "code": choice.value,
                    "name": str(choice.label),
                    "category": category,
                    "category_name": category_label,
                }
            )

        return success_response(
            data=data,
            request=request,
        )


@extend_schema(
    tags=("Organization Onboarding",),
    responses=SaaSPlanSerializer(many=True),
)
class SaaSPlanListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(
        self,
        request: Request,
    ) -> Response:
        category = (
            str(
                request.query_params.get(
                    "category",
                )
                or ""
            )
            .strip()
            .lower()
        )

        organization_type = (
            str(
                request.query_params.get(
                    "organization_type",
                )
                or ""
            )
            .strip()
            .lower()
        )

        size = (
            str(
                request.query_params.get(
                    "size",
                )
                or ""
            )
            .strip()
            .lower()
        )

        queryset: QuerySet[Plan] = Plan.objects.filter(
            is_active=True,
            is_public=True,
        ).order_by(
            "display_order",
            "price",
            "name",
        )

        if category and organization_type and size:
            eligible_ids = [
                plan.pk
                for plan in queryset
                if plan_is_eligible_for_onboarding(
                    plan,
                    category=category,
                    organization_type=organization_type,
                    size=size,
                )
            ]

            queryset = queryset.filter(
                pk__in=eligible_ids,
            )

        return success_response(
            data=SaaSPlanSerializer(
                queryset,
                many=True,
            ).data,
            request=request,
        )


@extend_schema(
    tags=("Organization Onboarding",),
    request=OrganizationPreflightSerializer,
)
class OrganizationRegistrationPreflightAPIView(
    OrganizationOnboardingContextMixin,
    APIView,
):
    permission_classes = (IsAuthenticated,)

    def post(
        self,
        request: Request,
    ) -> Response:
        serializer = OrganizationPreflightSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        try:
            result = OrganizationRegistrationOrchestrator.preflight(
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

        return success_response(
            data={
                "eligible": result.eligible,
                "organization_type": result.organization_type,
                "category": result.category,
                "size": result.size,
                "plan": result.plan,
                "payment_required": result.payment_required,
                "verification_required": result.verification_required,
                "next_step": result.next_step,
                "errors": list(result.errors),
            },
            request=request,
        )


@extend_schema(
    tags=("Organization Onboarding",),
    request=OrganizationOnboardingSerializer,
)
class RegisterOrganizationAPIView(
    OrganizationOnboardingContextMixin,
    APIView,
):
    permission_classes = (IsAuthenticated,)

    def post(
        self,
        request: Request,
    ) -> Response:
        serializer = OrganizationOnboardingSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        tenant = self.get_owner_tenant(
            request,
        )

        validated = dict(
            serializer.validated_data,
        )

        plan_id = validated.pop(
            "plan_id",
            None,
        )

        plan_code = validated.pop(
            "plan_code",
            None,
        )

        workflow_request = OrganizationOnboardingRequest(
            tenant=tenant,
            organization_data=validated,
            plan_id=plan_id,
            plan_code=plan_code or None,
            owner_user=request.user,
            metadata={
                "request_id": str(
                    getattr(
                        request,
                        "request_id",
                        "",
                    )
                    or ""
                ),
                "idempotency_key": str(
                    request.headers.get(
                        "Idempotency-Key",
                        "",
                    )
                    or ""
                ),
            },
        )

        try:
            result = OrganizationRegistrationOrchestrator.register(
                request=workflow_request,
            )
        except PermissionError as exc:
            return Response(
                {
                    "success": False,
                    "code": "permission_denied",
                    "detail": str(exc),
                },
                status=403,
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
        except OrganizationRegistrationError as exc:
            return Response(
                {
                    "success": False,
                    "code": "organization_registration_error",
                    "detail": str(exc),
                },
                status=400,
            )

        return success_response(
            data=result.as_dict(),
            request=request,
            status_code=(201 if result.onboarding.created_organization else 200),
            message=("Organization registration completed successfully."),
        )


@extend_schema(
    tags=("Organization Onboarding",),
)
class OrganizationOnboardingStatusAPIView(
    OrganizationOnboardingContextMixin,
    APIView,
):
    permission_classes = (IsAuthenticated,)

    def get(
        self,
        request: Request,
    ) -> Response:
        tenant = self.get_owner_tenant(
            request,
        )

        organizations = (
            Organization.objects.filter(
                tenant=tenant,
            )
            .select_related(
                "saas_subscription__plan",
            )
            .order_by(
                "name",
            )
        )

        data = []

        for organization in organizations:
            subscription = getattr(
                organization,
                "saas_subscription",
                None,
            )

            admin_assignment = OrganizationRole.objects.filter(
                organization=organization,
                user=request.user,
                role__code="organization_admin",
                is_active=True,
            ).exists()

            data.append(
                {
                    "organization": {
                        "id": str(
                            organization.pk,
                        ),
                        "name": organization.name,
                        "display_name": organization.display_name,
                        "code": organization.code,
                        "slug": organization.slug,
                        "category": organization.category,
                        "organization_type": organization.organization_type,
                        "size": organization.size,
                    },
                    "subscription": (
                        None
                        if subscription is None
                        else {
                            "id": str(
                                subscription.pk,
                            ),
                            "status": subscription.status,
                            "plan": {
                                "id": str(
                                    subscription.plan_id,
                                ),
                                "code": subscription.plan.code,
                                "name": subscription.plan.name,
                                "healthcare_segment": (
                                    subscription.plan.healthcare_segment
                                ),
                            },
                        }
                    ),
                    "organization_admin": admin_assignment,
                    "workspace": "organization",
                }
            )

        return success_response(
            data=data,
            request=request,
        )


__all__ = [
    "OrganizationOnboardingStatusAPIView",
    "OrganizationRegistrationPreflightAPIView",
    "OrganizationTypeListAPIView",
    "RegisterOrganizationAPIView",
    "SaaSPlanListAPIView",
]
