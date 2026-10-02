"""
SaaS Billing Subscription API views.

Handles:

- Subscription retrieval
- Subscription creation
- Activation
- Renewal
- Cancellation

Architecture:

API
 |
Organization Context
 |
RBAC
 |
Workflow Registry
 |
Subscription Workflow
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    success_response,
)
from apps.platform.saas_billing.api.mixins import (
    OrganizationContextMixin,
)
from apps.platform.saas_billing.api.permissions import (
    CanManageSubscription,
    CanViewSubscription,
)
from apps.platform.saas_billing.api.serializers import (
    SubscriptionCreateSerializer,
    SubscriptionLifecycleSerializer,
    SubscriptionSerializer,
)
from apps.platform.saas_billing.models import (
    Plan,
    Subscription,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)


class SubscriptionDetailAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Retrieve current organization subscription.
    """

    permission_classes = [
        CanViewSubscription,
    ]

    def get(
        self,
        request,
    ):

        organization = self.get_organization(
            request,
        )

        if not organization:
            return Response(
                {"detail": ("Organization context missing.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = (
            Subscription.objects.filter(
                organization=organization,
            )
            .select_related(
                "plan",
            )
            .first()
        )

        if not subscription:
            return Response(
                {"detail": ("Subscription not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        return success_response(
            data=SubscriptionSerializer(
                subscription,
            ).data,
        )


class SubscriptionCreateAPIView(
    OrganizationContextMixin,
    APIView,
):
    permission_classes = [
        CanManageSubscription,
    ]

    def post(
        self,
        request,
    ):

        organization = self.get_organization(
            request,
        )

        if not organization:
            return Response(
                {"detail": ("Organization context missing.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubscriptionCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        plan = None

        plan_id = serializer.validated_data.get(
            "plan_id",
        )

        if plan_id:
            plan = Plan.objects.filter(
                id=plan_id,
                is_active=True,
            ).first()

            if not plan:
                return Response(
                    {"detail": ("Invalid subscription plan.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        subscription = WorkflowRegistry.execute(
            "subscription.create",
            organization=organization,
            plan=plan,
        )

        return success_response(
            data=SubscriptionSerializer(
                subscription,
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class SubscriptionActivateAPIView(
    OrganizationContextMixin,
    APIView,
):
    permission_classes = [
        CanManageSubscription,
    ]

    def post(
        self,
        request,
    ):

        subscription = self._get_subscription(
            request,
        )

        subscription = WorkflowRegistry.execute(
            "subscription.activate",
            subscription=subscription,
        )

        return success_response(
            data=SubscriptionSerializer(
                subscription,
            ).data,
        )

    def _get_subscription(
        self,
        request,
    ):

        return Subscription.objects.get(
            organization=self.get_organization(
                request,
            )
        )


class SubscriptionRenewAPIView(
    OrganizationContextMixin,
    APIView,
):
    permission_classes = [
        CanManageSubscription,
    ]

    def post(
        self,
        request,
    ):

        subscription = Subscription.objects.get(
            organization=self.get_organization(
                request,
            ),
        )

        subscription = WorkflowRegistry.execute(
            "subscription.renew",
            subscription=subscription,
        )

        return success_response(
            data=SubscriptionSerializer(
                subscription,
            ).data,
        )


class SubscriptionCancelAPIView(
    OrganizationContextMixin,
    APIView,
):
    permission_classes = [
        CanManageSubscription,
    ]

    def post(
        self,
        request,
    ):

        serializer = SubscriptionLifecycleSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        subscription = Subscription.objects.get(
            organization=self.get_organization(
                request,
            ),
        )

        subscription = WorkflowRegistry.execute(
            "subscription.cancel",
            subscription=subscription,
            reason=(
                serializer.validated_data.get(
                    "reason",
                )
            ),
        )

        return success_response(
            data=SubscriptionSerializer(
                subscription,
            ).data,
        )


__all__ = (
    "SubscriptionDetailAPIView",
    "SubscriptionCreateAPIView",
    "SubscriptionActivateAPIView",
    "SubscriptionRenewAPIView",
    "SubscriptionCancelAPIView",
)
