"""
Base test utilities for DatavionOS SaaS Billing.

Provides reusable setup for:

- Tenant
- Organization
- User
- RBAC
- Plan
- Subscription
- API Authentication Context

All SaaS billing tests inherit from this class.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.constants import (
    PermissionScope,
)
from apps.platform.rbac.models import (
    OrganizationRole,
    Permission,
    Role,
    RolePermission,
    UserRole,
)
from apps.platform.saas_billing.models import (
    Plan,
    Subscription,
)
from apps.platform.tenancy.models import Tenant


class SaaSBillingTestBase(
    TestCase,
):
    """
    Common SaaS billing test foundation.
    """

    def setUp(
        self,
    ):
        """
        Prepare billing test environment.
        """

        super().setUp()

        self.tenant = self.create_tenant()

        self.user = self.create_user()

        self.organization = self.create_organization()

        self.role = self.create_billing_role()

        self.assign_billing_permissions()

        self.assign_user_role()

        self.assign_organization_role()

        self.plan = self.create_plan()

        self.subscription = self.create_subscription()

    # ==========================================================
    # API AUTH CONTEXT
    # ==========================================================

    def authenticate_api_client(
        self,
    ):
        """
        Authenticate API client with
        DatavionOS organization context.

        Simulates organization middleware.
        """

        self.client.force_authenticate(
            user=self.user,
        )

        self.client.credentials(
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
        )

    # ==========================================================
    # TENANT
    # ==========================================================

    def create_tenant(
        self,
    ) -> Tenant:

        return Tenant.objects.create(
            name="Apollo Demo Tenant",
            slug="apollo-demo-tenant",
        )

    # ==========================================================
    # USER
    # ==========================================================

    def create_user(
        self,
    ) -> User:

        return User.objects.create_user(
            email="admin@datavion.com",
            password="Test@12345",
        )

    # ==========================================================
    # ORGANIZATION
    # ==========================================================

    def create_organization(
        self,
    ) -> Organization:

        return Organization.objects.create(
            tenant=self.tenant,
            name="Apollo Demo Hospital",
            display_name="Apollo Demo Hospital",
            code="APOLLO-E2E",
            email="admin@apollo.com",
        )

    # ==========================================================
    # RBAC ROLE
    # ==========================================================

    def create_billing_role(
        self,
    ) -> Role:

        return Role.objects.create(
            name="Billing Administrator",
            code="billing-admin-test",
            description=("Billing administrator role for SaaS billing tests."),
            is_system=False,
            is_active=True,
        )

    # ==========================================================
    # RBAC PERMISSIONS
    # ==========================================================

    def assign_billing_permissions(
        self,
    ):
        """
        Create SaaS billing permissions.
        """

        permissions = [
            "billing.view",
            "subscriptions.view",
            "invoices.view",
            "payments.view",
            "usage.view",
        ]

        for code in permissions:
            module, action = code.split(
                ".",
                1,
            )

            permission, _ = Permission.objects.get_or_create(
                code=code,
                defaults={
                    "name": (
                        code.replace(
                            ".",
                            " ",
                        ).title()
                    ),
                    "module": module,
                    "action": action,
                    "scope": (PermissionScope.ORGANIZATION),
                    "is_system": False,
                    "is_assignable": True,
                },
            )

            RolePermission.objects.get_or_create(
                role=self.role,
                permission=permission,
            )

    # ==========================================================
    # USER ROLE
    # ==========================================================

    def assign_user_role(
        self,
    ):

        UserRole.objects.create(
            user=self.user,
            role=self.role,
            is_active=True,
        )

    # ==========================================================
    # ORGANIZATION ROLE
    # ==========================================================

    def assign_organization_role(
        self,
    ):

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=self.role,
            is_primary=True,
            is_active=True,
        )

    # ==========================================================
    # PLAN
    # ==========================================================

    def create_plan(
        self,
    ) -> Plan:

        return Plan.objects.create(
            name="Enterprise Healthcare AI",
            code="enterprise-healthcare-ai-test",
            price=Decimal(
                "9999.00",
            ),
            currency="INR",
            billing_cycle=(Plan.BillingCycle.MONTHLY),
            limits={
                "users": 10,
                "patients": 1000,
                "storage_gb": 50,
                "AI_REQUESTS": {
                    "included": 1000,
                    "unit": "request",
                },
            },
            modules={
                "ai": True,
                "billing": True,
                "clinical": True,
            },
            features={
                "advanced_ai": True,
                "telemedicine": True,
                "analytics": True,
            },
        )

    # ==========================================================
    # SUBSCRIPTION
    # ==========================================================

    def create_subscription(
        self,
    ) -> Subscription:

        now = timezone.now()

        return Subscription.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            plan=self.plan,
            status=(Subscription.Status.ACTIVE),
            auto_renew=True,
            started_at=now,
            current_period_start=now,
            current_period_end=(
                now
                + timedelta(
                    days=30,
                )
            ),
            plan_snapshot={
                "name": (self.plan.name),
                "price": ("9999.00"),
                "limits": self.plan.limits,
            },
            feature_snapshot={
                "modules": (self.plan.modules),
                "features": (self.plan.features),
            },
        )
