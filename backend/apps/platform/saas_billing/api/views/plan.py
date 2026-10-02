"""
DatavionOS SaaS Billing Plan API views.

Handles:

- Public plan catalog
- Plan details
- Plan creation
- Plan updates
- Plan activation
- Plan deactivation
- Plan archive

Architecture:

API
 |
RBAC
 |
Serializer
 |
Workflow Registry
 |
Plan Workflow
 |
Plan Service
 |
Domain Event
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    success_response,
)
from apps.platform.saas_billing.api.mixins import (
    PlanLookupMixin,
)
from apps.platform.saas_billing.api.permissions import (
    CanManagePlan,
    CanViewPlan,
)
from apps.platform.saas_billing.api.serializers import (
    PlanAdminSerializer,
    PlanCreateSerializer,
    PlanDetailSerializer,
    PlanUpdateSerializer,
    PublicPlanSerializer,
)
from apps.platform.saas_billing.models import (
    Plan,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)

# =============================================================================
# Public Plan APIs
# =============================================================================


class PlanListAPIView(
    APIView,
):
    """
    Retrieve public SaaS plans.

    GET /billing/plans/
    """

    permission_classes = [
        CanViewPlan,
    ]

    def get(
        self,
        request,
    ):

        plans = Plan.objects.filter(
            is_active=True,
            is_public=True,
        ).order_by(
            "display_order",
            "price",
        )

        return success_response(
            data=PublicPlanSerializer(
                plans,
                many=True,
            ).data,
        )


class PlanDetailAPIView(
    APIView,
):
    """
    Retrieve SaaS plan details.

    GET /billing/plans/<uuid>/
    """

    permission_classes = [
        CanViewPlan,
    ]

    def get(
        self,
        request,
        pk,
    ):

        plan = Plan.objects.filter(
            id=pk,
            is_active=True,
        ).first()

        if not plan:
            return Response(
                {
                    "detail": "Plan not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            PlanDetailSerializer(
                plan,
            ).data,
            status=status.HTTP_200_OK,
        )


# =============================================================================
# Plan Management APIs
# =============================================================================


class PlanCreateAPIView(
    APIView,
):
    """
    Create SaaS plan.

    POST /billing/plans/create/
    """

    permission_classes = [
        CanManagePlan,
    ]

    def post(
        self,
        request,
    ):

        serializer = PlanCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        plan = WorkflowRegistry.execute(
            "plan.create",
            data=serializer.validated_data,
        )

        return Response(
            PlanAdminSerializer(
                plan,
            ).data,
            status=status.HTTP_201_CREATED,
        )


class PlanUpdateAPIView(
    PlanLookupMixin,
    APIView,
):
    """
    Update SaaS plan.

    PATCH /billing/plans/<uuid>/update/
    """

    permission_classes = [
        CanManagePlan,
    ]

    def patch(
        self,
        request,
        pk,
    ):

        plan = self.get_plan(
            pk,
        )

        serializer = PlanUpdateSerializer(
            plan,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        plan = WorkflowRegistry.execute(
            "plan.update",
            plan=plan,
            data=serializer.validated_data,
        )

        return Response(
            PlanAdminSerializer(
                plan,
            ).data,
            status=status.HTTP_200_OK,
        )


class PlanActivateAPIView(
    PlanLookupMixin,
    APIView,
):
    """
    Activate SaaS plan.

    POST /billing/plans/<uuid>/activate/
    """

    permission_classes = [
        CanManagePlan,
    ]

    def post(
        self,
        request,
        pk,
    ):

        plan = self.get_plan(
            pk,
        )

        plan = WorkflowRegistry.execute(
            "plan.activate",
            plan=plan,
        )

        return success_response(
            data=PlanAdminSerializer(
                plan,
            ).data,
        )


class PlanDeactivateAPIView(
    PlanLookupMixin,
    APIView,
):
    """
    Deactivate SaaS plan.

    POST /billing/plans/<uuid>/deactivate/
    """

    permission_classes = [
        CanManagePlan,
    ]

    def post(
        self,
        request,
        pk,
    ):

        plan = self.get_plan(
            pk,
        )

        plan = WorkflowRegistry.execute(
            "plan.deactivate",
            plan=plan,
        )

        return success_response(
            data=PlanAdminSerializer(
                plan,
            ).data,
        )


class PlanArchiveAPIView(
    PlanLookupMixin,
    APIView,
):
    """
    Archive SaaS plan.

    POST /billing/plans/<uuid>/archive/
    """

    permission_classes = [
        CanManagePlan,
    ]

    def post(
        self,
        request,
        pk,
    ):

        plan = self.get_plan(
            pk,
        )

        plan = WorkflowRegistry.execute(
            "plan.archive",
            plan=plan,
        )

        return success_response(
            data=PlanAdminSerializer(
                plan,
            ).data,
        )


__all__ = (
    "PlanListAPIView",
    "PlanDetailAPIView",
    "PlanCreateAPIView",
    "PlanUpdateAPIView",
    "PlanActivateAPIView",
    "PlanDeactivateAPIView",
    "PlanArchiveAPIView",
)
