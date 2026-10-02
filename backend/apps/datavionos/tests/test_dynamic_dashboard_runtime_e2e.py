from __future__ import annotations

import os
from uuid import uuid4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from unittest.mock import patch

from django.test import TestCase

from apps.datavionos.bootstrap.service import PlatformBootstrapService
from apps.datavionos.onboarding.contracts import OrganizationOnboardingRequest
from apps.datavionos.onboarding.workflow import RegisterOrganizationWorkflow
from apps.datavionos.selectors.module_availability import module_availability_selector
from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)
from apps.datavionos.services.saas_capability_control_plane import get_provider
from apps.platform.accounts.services.authentication import AuthenticationService
from apps.platform.accounts.services.otp import OTPService
from apps.platform.organizations.models import OrganizationModule
from apps.platform.organizations.services.organization_module import (
    disable_module,
    enable_module,
)
from apps.platform.saas_billing.models import Plan
from apps.platform.tenancy.context import TenantContext, set_tenant_context
from apps.platform.tenancy.models import TenantMembership
from apps.platform.tenancy.services.tenant import TenantService


class DynamicDashboardRuntimeE2ETests(TestCase):
    # Real database-backed lifecycle test.
    # All onboarding, subscription, entitlement, provider, module-toggle,
    # and bootstrap components execute for real. Only OTP entropy is
    # deterministic so the test can verify the real OTP workflow without
    # reading a secret/hash from the database.

    def setUp(self):
        self.suffix = uuid4().hex[:10]
        self.email = f"runtime-e2e-{self.suffix}@example.test"
        self.password = "RuntimeE2E!Password123"

    def register_and_login(self):
        user = AuthenticationService.register(
            username=self.email,
            email=self.email,
            first_name="Runtime",
            last_name="E2E",
            password=self.password,
            is_active=True,
        )

        # The test account is verified after exercising registration.
        user.is_verified = True
        user.save(update_fields=["is_verified", "updated_at"])

        # OTPService persists only a hash, so the database model intentionally
        # has no plaintext ``code`` field. Make OTP generation deterministic
        # for this test and execute the real request/verify services.
        with patch.object(
            OTPService,
            "generate_code",
            return_value="123456",
        ):
            login_otp = AuthenticationService.request_login_otp(
                email=self.email,
                password=self.password,
            )

            tokens = AuthenticationService.verify_login_otp(
                otp_id=login_otp["otp_id"],
                code="123456",
                ip_address="127.0.0.1",
                device="DatavionOS E2E",
                location="test",
            )

        self.assertIn("access", tokens)
        return user.__class__.objects.get(pk=user.pk)

    def create_plan(self):
        return Plan.objects.create(
            name=f"Runtime E2E {self.suffix}",
            code=f"runtime-e2e-{self.suffix}",
            healthcare_segment="CLINIC",
            plan_type="starter",
            price=0,
            setup_fee=0,
            trial_days=14,
            modules={"patients": True},
            features={"patients.dashboard": True},
            limits={"patients": {"included": 100}},
            is_active=True,
            is_public=True,
            is_default=False,
            is_custom=True,
        )

    def test_pharmacy_tenant_receives_pharmacy_module(self):
        tenant = type(
            "TenantStub",
            (),
            {
                "tenant_type": "pharmacy",
                "organizations": type(
                    "OrgManager",
                    (),
                    {"first": lambda self: object()},
                )(),
            },
        )()

        capabilities = {"modules": {"pharmacy": True}}
        modules = module_availability_selector.get(
            tenant=tenant,
            capabilities=capabilities,
        )

        self.assertTrue(
            any(module.identifier == "pharmacy" for module in modules),
            msg=f"Expected pharmacy module to be available for pharmacy tenant; got {[module.identifier for module in modules]}",
        )

    def test_register_login_onboard_bootstrap_disable_reenable(self):
        user = self.register_and_login()

        tenant = TenantService.create_tenant(
            name=f"Runtime E2E Tenant {self.suffix}",
            slug=f"runtime-e2e-{self.suffix}",
            tenant_type="clinic",
            owner=user,
        )

        plan = self.create_plan()

        result = RegisterOrganizationWorkflow(
            request=OrganizationOnboardingRequest(
                tenant=tenant,
                organization_data={
                    "name": f"Runtime E2E Clinic {self.suffix}",
                    "display_name": f"Runtime E2E Clinic {self.suffix}",
                    "code": f"rte2e{self.suffix}",
                    "slug": f"runtime-e2e-clinic-{self.suffix}",
                    "organization_type": "CLINIC",
                },
                plan_id=plan.pk,
            )
        ).handle()

        organization = result.organization

        self.assertTrue(result.created_organization)
        self.assertTrue(result.created_subscription)
        self.assertEqual(result.subscription.plan_id, plan.pk)
        self.assertIn("patients", result.modules)

        membership = TenantMembership.objects.get(
            tenant=tenant,
            user=user,
        )
        self.assertTrue(membership.is_owner)

        module = OrganizationModule.objects.get(
            organization=organization,
            module_code="patients",
        )
        self.assertEqual(
            module.status,
            OrganizationModule.Status.ENABLED,
        )

        set_tenant_context(
            TenantContext(
                tenant=tenant,
                user=user,
                membership=membership,
            )
        )

        snapshot = get_provider().resolve(
            user=user,
            organization=organization,
        )

        self.assertTrue(snapshot.modules.get("patients"))
        self.assertTrue(snapshot.features.get("patients.dashboard"))

        effective = build_effective_capability_context(
            user_id=str(user.pk),
            organization_id=str(organization.pk),
            tenant_id=str(tenant.pk),
            modules=snapshot.modules,
            features=snapshot.features,
            permissions=snapshot.permissions,
        )
        self.assertTrue(effective.module_enabled("patients"))
        self.assertTrue(effective.feature_enabled("patients.dashboard"))

        bootstrap = PlatformBootstrapService().bootstrap(
            user=user,
            tenant=tenant,
            organization=organization,
            permissions=set(snapshot.permissions),
        )

        visible = {
            getattr(item, "identifier", getattr(item, "module_code", ""))
            for item in (bootstrap.modules or [])
        }
        if "patients" not in visible:
            selector_capabilities = {
                "modules": dict(snapshot.modules),
                "features": dict(snapshot.features),
            }
            selector_modules = module_availability_selector.get(
                tenant=tenant,
                capabilities=selector_capabilities,
            )
            service_probe = PlatformBootstrapService()
            service_selector_modules = service_probe._module_selector.get(
                tenant=tenant,
                capabilities=selector_capabilities,
            )
            service_method_modules = service_probe._bootstrap_modules(
                tenant=tenant,
                capabilities=selector_capabilities,
            )
            tenant_org_relation = getattr(tenant, "organizations", None)
            tenant_org = None
            tenant_org_error = None
            if tenant_org_relation is not None:
                try:
                    tenant_org = tenant_org_relation.first()
                except Exception as exc:
                    tenant_org_error = f"{type(exc).__name__}: {exc}"
            self.fail(
                "Patients missing from bootstrap. "
                f"tenant_id={tenant.pk}; tenant_type={getattr(tenant, 'tenant_type', None)!r}; "
                f"explicit_organization_id={getattr(organization, 'pk', None)!r}; "
                f"tenant.organizations_exists={tenant_org_relation is not None}; "
                f"tenant_organization_id={getattr(tenant_org, 'pk', None)!r}; "
                f"tenant_organization_error={tenant_org_error!r}; "
                f"snapshot_modules={dict(snapshot.modules)!r}; "
                f"selector_modules={[m.identifier for m in selector_modules]!r}; "
                f"service_selector_type={type(service_probe._module_selector).__name__!r}; "
                f"service_selector_is_global={service_probe._module_selector is module_availability_selector}; "
                f"service_selector_modules={[m.identifier for m in service_selector_modules]!r}; "
                f"service_method_modules={[m.identifier for m in service_method_modules]!r}; "
                f"bootstrap_modules={[getattr(m, 'identifier', getattr(m, 'module_code', '')) for m in (bootstrap.modules or [])]!r}"
            )

        disable_module(instance=module)

        disabled = get_provider().resolve(
            user=user,
            organization=organization,
        )
        disabled_context = build_effective_capability_context(
            user_id=str(user.pk),
            organization_id=str(organization.pk),
            tenant_id=str(tenant.pk),
            modules=disabled.modules,
            features=disabled.features,
            permissions=disabled.permissions,
        )
        self.assertFalse(disabled_context.module_enabled("patients"))

        disabled_bootstrap = PlatformBootstrapService().bootstrap(
            user=user,
            tenant=tenant,
            organization=organization,
            permissions=set(disabled.permissions),
        )
        disabled_visible = {
            getattr(item, "identifier", getattr(item, "module_code", ""))
            for item in (disabled_bootstrap.modules or [])
        }
        self.assertNotIn("patients", disabled_visible)

        enable_module(instance=module)

        enabled = get_provider().resolve(
            user=user,
            organization=organization,
        )
        enabled_context = build_effective_capability_context(
            user_id=str(user.pk),
            organization_id=str(organization.pk),
            tenant_id=str(tenant.pk),
            modules=enabled.modules,
            features=enabled.features,
            permissions=enabled.permissions,
        )
        self.assertTrue(enabled_context.module_enabled("patients"))

        enabled_bootstrap = PlatformBootstrapService().bootstrap(
            user=user,
            tenant=tenant,
            organization=organization,
            permissions=set(enabled.permissions),
        )
        enabled_visible = {
            getattr(item, "identifier", getattr(item, "module_code", ""))
            for item in (enabled_bootstrap.modules or [])
        }
        self.assertIn("patients", enabled_visible)
