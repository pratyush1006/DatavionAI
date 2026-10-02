"""
DatavionOS SaaS Subscription Runtime API.

Read-only runtime context endpoint for the authenticated
organization subscription.
"""

from __future__ import annotations

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.platform.saas_billing.models.subscription import Subscription


class SubscriptionRuntimeAPIView(APIView):
    """
    Return the current authenticated organization's subscription
    together with its plan, usage, feature, and plan snapshots.
    """

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> JsonResponse:
        """
        Return the active subscription runtime context.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        if organization is None:
            user = getattr(
                request,
                "user",
                None,
            )

            organization = getattr(
                user,
                "organization",
                None,
            )

        if organization is None:
            return JsonResponse(
                {
                    "detail": "No active organization context.",
                    "subscription": None,
                },
                status=404,
            )

        subscription = (
            Subscription.objects.select_related("plan")
            .filter(
                organization=organization,
            )
            .first()
        )

        if subscription is None:
            return JsonResponse(
                {
                    "detail": "No subscription found.",
                    "subscription": None,
                },
                status=404,
            )

        plan = subscription.plan

        return JsonResponse(
            {
                "subscription": {
                    "id": str(subscription.id),
                    "status": subscription.status,
                    "auto_renew": subscription.auto_renew,
                    "trial_start": (
                        subscription.trial_start.isoformat()
                        if subscription.trial_start
                        else None
                    ),
                    "trial_end": (
                        subscription.trial_end.isoformat()
                        if subscription.trial_end
                        else None
                    ),
                    "current_period_start": (
                        subscription.current_period_start.isoformat()
                        if subscription.current_period_start
                        else None
                    ),
                    "current_period_end": (
                        subscription.current_period_end.isoformat()
                        if subscription.current_period_end
                        else None
                    ),
                    "expires_at": (
                        subscription.expires_at.isoformat()
                        if subscription.expires_at
                        else None
                    ),
                    "plan": {
                        "id": str(plan.id),
                        "name": plan.name,
                        "code": plan.code,
                        "plan_type": plan.plan_type,
                        "healthcare_segment": (plan.healthcare_segment),
                        "price": str(plan.price),
                        "setup_fee": str(plan.setup_fee),
                        "currency": plan.currency,
                        "billing_cycle": plan.billing_cycle,
                        "trial_days": plan.trial_days,
                        "annual_discount_percentage": (plan.annual_discount_percentage),
                        "is_custom": plan.is_custom,
                        "features": plan.features,
                        "modules": plan.modules,
                        "limits": plan.limits,
                    },
                    "usage": {
                        "seats_used": subscription.seats_used,
                        "usage_snapshot": (subscription.usage_snapshot),
                    },
                    "feature_snapshot": (subscription.feature_snapshot),
                    "plan_snapshot": (subscription.plan_snapshot),
                },
            },
            status=200,
        )


# Backward-compatible canonical export.
#
# Existing API consumers and views/__init__.py use the historical
# CurrentSubscriptionAPIView name. Keep it as an alias so there is
# exactly one implementation of the runtime endpoint.
CurrentSubscriptionAPIView = SubscriptionRuntimeAPIView


__all__ = [
    "SubscriptionRuntimeAPIView",
    "CurrentSubscriptionAPIView",
]
