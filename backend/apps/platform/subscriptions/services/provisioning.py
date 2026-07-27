"""
Subscription provisioning services.

Handles tenant subscription activation.

Plan entitlements are managed separately
from tenant subscription assignment.

Architecture:

SubscriptionPlan
        |
        +--> ModuleEntitlements
        |
        +--> FeatureEntitlements


Tenant
        |
        v
TenantSubscription
        |
        v
SubscriptionPlan
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.platform.subscriptions.models import (
    SubscriptionPlan,
    TenantSubscription,
)
from apps.platform.tenancy.models import Tenant


class SubscriptionProvisioningService:
    """
    Provision SaaS subscription for tenants.
    """

    @transaction.atomic
    def activate_plan(
        self,
        *,
        tenant: Tenant,
        plan: SubscriptionPlan,
    ) -> TenantSubscription:
        """
        Activate subscription plan for tenant.

        Creates or updates tenant subscription.
        """

        subscription, _ = TenantSubscription.objects.update_or_create(
            tenant=tenant,
            defaults={
                "plan": plan,
                "status": (TenantSubscription.Status.ACTIVE),
                "starts_at": timezone.now(),
                "auto_renew": True,
            },
        )

        return subscription

    @transaction.atomic
    def provision_plan(
        self,
        *,
        tenant: Tenant,
        plan: SubscriptionPlan,
    ) -> TenantSubscription:
        """
        Assign subscription plan to tenant.

        Plan entitlements are not created here.

        They belong to SubscriptionPlan and are
        managed through plan configuration.

        Flow:

        SubscriptionPlan
              |
              v
        ModuleEntitlements
        FeatureEntitlements


        Tenant
              |
              v
        TenantSubscription
        """

        return self.activate_plan(
            tenant=tenant,
            plan=plan,
        )


subscription_provisioning_service = SubscriptionProvisioningService()


__all__ = [
    "SubscriptionProvisioningService",
    "subscription_provisioning_service",
]
