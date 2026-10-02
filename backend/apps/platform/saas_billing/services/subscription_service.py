"""
Subscription services.

Business logic layer for DatavionOS SaaS subscriptions.

Responsibilities:

- Create subscriptions
- Assign plans
- Trial lifecycle
- Activation
- Renewal
- Cancellation
- Plan migration
- Feature/module entitlement management

Architecture:

Organization
      |
SubscriptionService
      |
Subscription Workflow
      |
Subscription Model
      |
Entitlements
      |
Platform Bootstrap
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.saas_billing.models import (
    Plan,
    Subscription,
)


class SubscriptionService:
    """
    Enterprise SaaS subscription service.
    """

    # ------------------------------------------------------------------
    # Snapshot Builder
    # ------------------------------------------------------------------

    @staticmethod
    def _build_plan_snapshot(
        plan: Plan,
    ) -> dict:
        """
        Build immutable plan snapshot.

        Snapshot stores customer entitlement
        configuration at subscription creation time.

        Includes:

        - Pricing
        - Billing cycle
        - Resource limits
        - Usage limits
        - Modules
        - Features
        - Metadata
        """

        return {
            "name": plan.name,
            "code": plan.code,
            "price": str(
                plan.price,
            ),
            "currency": plan.currency,
            "billing_cycle": (plan.billing_cycle),
            "limits": {
                # Platform limits
                "users": (plan.max_users),
                "branches": (plan.max_branches),
                "doctors": (plan.max_doctors),
                "patients": (plan.max_patients),
                "storage_gb": (plan.max_storage_gb),
                # Dynamic SaaS usage limits
                #
                # Example:
                #
                # {
                #     "AI_REQUEST": {
                #         "included": 1000,
                #         "overage_rate": "0.02",
                #         "unit": "request"
                #     }
                # }
                **(plan.limits or {}),
            },
            "modules": (plan.modules),
            "features": (plan.features),
            "metadata": (plan.metadata),
        }

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def create_trial_subscription(
        *,
        organization: Organization,
        plan: Plan,
    ) -> Subscription:
        """
        Create trial subscription.
        """

        existing = Subscription.objects.filter(
            organization=organization,
        ).first()

        if existing:
            return existing

        now = timezone.now()

        is_free_plan = Decimal(str(plan.price or 0)) <= Decimal("0")
        # A paid plan must never silently become a trial merely because its
        # catalog record carries trial_days.  Paid access is activated only by
        # the payment lifecycle; free plans may use an explicit trial window.
        has_trial = is_free_plan and plan.trial_days > 0
        trial_end = now + timedelta(days=plan.trial_days) if has_trial else None
        status = (
            Subscription.Status.TRIAL
            if has_trial
            else Subscription.Status.ACTIVE
            if is_free_plan
            else Subscription.Status.PAST_DUE
        )

        snapshot = SubscriptionService._build_plan_snapshot(
            plan,
        )

        return Subscription.objects.create(
            tenant=(organization.tenant),
            organization=organization,
            plan=plan,
            status=status,
            trial_start=now if has_trial else None,
            trial_end=trial_end,
            started_at=now if status == Subscription.Status.ACTIVE else None,
            current_period_start=now,
            current_period_end=trial_end,
            plan_snapshot=snapshot,
            feature_snapshot={
                "modules": (plan.modules),
                "features": (plan.features),
            },
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Activate subscription.
        """

        now = timezone.now()

        subscription.status = Subscription.Status.ACTIVE

        subscription.started_at = subscription.started_at or now

        subscription.save(
            update_fields=[
                "status",
                "started_at",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def renew(
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Renew subscription period.
        """

        start = timezone.now()

        days = 365 if subscription.plan.billing_cycle == "yearly" else 30

        end = start + timedelta(
            days=days,
        )

        subscription.status = Subscription.Status.ACTIVE

        subscription.current_period_start = start

        subscription.current_period_end = end

        subscription.expires_at = end

        subscription.save(
            update_fields=[
                "status",
                "current_period_start",
                "current_period_end",
                "expires_at",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def cancel(
        *,
        subscription: Subscription,
        reason=(Subscription.CancellationReason.CUSTOMER_REQUEST),
    ) -> Subscription:
        """
        Cancel subscription.
        """

        subscription.status = Subscription.Status.CANCELLED

        subscription.auto_renew = False

        subscription.cancelled_at = timezone.now()

        subscription.cancellation_reason = (
            reason or Subscription.CancellationReason.CUSTOMER_REQUEST
        )

        subscription.save(
            update_fields=[
                "status",
                "auto_renew",
                "cancelled_at",
                "cancellation_reason",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def suspend(
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Suspend subscription.
        """

        subscription.status = Subscription.Status.SUSPENDED

        subscription.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def expire(
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Expire subscription.
        """

        subscription.status = Subscription.Status.EXPIRED

        subscription.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return subscription

    # ------------------------------------------------------------------
    # Plan Management
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def assign_plan(
        *,
        subscription: Subscription,
        plan: Plan,
    ) -> Subscription:
        """
        Assign new plan.
        """

        subscription.plan = plan

        subscription.plan_snapshot = SubscriptionService._build_plan_snapshot(
            plan,
        )

        subscription.feature_snapshot = {
            "modules": (plan.modules),
            "features": (plan.features),
        }

        subscription.save(
            update_fields=[
                "plan",
                "plan_snapshot",
                "feature_snapshot",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    def upgrade(
        *,
        subscription: Subscription,
        new_plan: Plan,
    ) -> Subscription:
        """
        Upgrade subscription.
        """

        return SubscriptionService.assign_plan(
            subscription=subscription,
            plan=new_plan,
        )

    @staticmethod
    def downgrade(
        *,
        subscription: Subscription,
        new_plan: Plan,
    ) -> Subscription:
        """
        Downgrade subscription.
        """

        return SubscriptionService.assign_plan(
            subscription=subscription,
            plan=new_plan,
        )

    # ------------------------------------------------------------------
    # Entitlements
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def refresh_entitlements(
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Refresh module and feature access.
        """

        subscription.feature_snapshot = {
            "modules": (subscription.plan.modules),
            "features": (subscription.plan.features),
        }

        subscription.save(
            update_fields=[
                "feature_snapshot",
                "updated_at",
            ],
        )

        return subscription

    @staticmethod
    def has_feature(
        *,
        subscription: Subscription,
        feature: str,
    ) -> bool:
        """
        Check feature access.
        """

        return bool(
            subscription.feature_snapshot.get(
                "features",
                {},
            ).get(
                feature,
                False,
            )
        )

    @staticmethod
    def has_module(
        *,
        subscription: Subscription,
        module: str,
    ) -> bool:
        """
        Check module access.
        """

        return bool(
            subscription.feature_snapshot.get(
                "modules",
                {},
            ).get(
                module,
                False,
            )
        )


__all__ = [
    "SubscriptionService",
]
