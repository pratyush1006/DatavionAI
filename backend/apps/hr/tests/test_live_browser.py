"""Opt-in real browser/API test against the disposable pytest database.

Run: $env:DATAVION_HR_LIVE='1'; python -m pytest apps/hr/tests/test_live_browser.py
Requires the frontend development server on localhost:3000.
"""

import json
import os
import subprocess
from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest
from django.apps import apps
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.hr.tests.test_recruitment import assign_hr_role
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization, OrganizationModule
from apps.platform.saas_billing.models import Plan, Subscription
from apps.platform.tenancy.models import Tenant, TenantMembership


@pytest.mark.skipif(
    os.environ.get("DATAVION_HR_LIVE") != "1", reason="Opt-in browser integration test"
)
@pytest.mark.django_db(
    transaction=True, available_apps=[config.name for config in apps.get_app_configs()]
)
def test_live_hr_browser(settings, request, transactional_db):
    settings.ROOT_URLCONF = "apps.hr.tests.live_urls"
    settings.SECURE_SSL_REDIRECT = False
    settings.ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
    suffix = uuid4().hex[:10]
    tenant = Tenant.objects.create(
        name="HR Browser",
        slug=f"hr-browser-{suffix}",
        tenant_type="clinic",
        status="ACTIVE",
    )
    organization = Organization.objects.create(
        tenant=tenant,
        name="HR Browser Hospital",
        code=f"HR{suffix}",
        slug=f"hr-browser-{suffix}",
        organization_type="CLINIC",
        status="ACTIVE",
    )
    user = assign_hr_role(organization, "hr_manager")
    user.organization = organization
    user.is_verified = True
    user.first_name = "HR"
    user.last_name = "Manager"
    user.save()
    TenantMembership.objects.create(tenant=tenant, user=user, status="active")
    employee = Employee.objects.create(
        organization=organization,
        user=user,
        employee_code="HR001",
        designation="HR Manager",
        joining_date=date(2025, 1, 1),
    )
    plan = Plan.objects.create(
        name=f"HR Browser {suffix}",
        code=f"hr-browser-{suffix}",
        modules={"hr": True},
        price=0,
    )
    Subscription.objects.create(
        tenant=tenant,
        organization=organization,
        plan=plan,
        status="ACTIVE",
        plan_snapshot={"modules": {"hr": True}},
        feature_snapshot={"modules": {"hr": True}},
    )
    OrganizationModule.objects.create(
        organization=organization, module_code="hr", status="enabled"
    )
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token.access_token}",
        HTTP_X_ORGANIZATION_ID=str(organization.pk),
    )
    response = client.get("/api/platform/bootstrap/")
    assert response.status_code == 200, response.data
    assert any(
        module["identifier"] == "hr" for module in response.data["data"]["modules"]
    ), response.data["data"]["modules"]
    assert "attendance.view" in response.data["data"]["permissions"]
    assert "employees.view" in response.data["data"]["permissions"]
    employees_response = client.get("/api/employees/")
    assert employees_response.status_code == 200, employees_response.data
    server = request.getfixturevalue("live_server")
    environment = {
        **os.environ,
        "HR_LIVE_API_URL": server.url,
        "HR_LIVE_SESSION": json.dumps(
            {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "current_user": {
                    "id": str(user.pk),
                    "email": user.email,
                    "first_name": "HR",
                    "last_name": "Manager",
                    "is_verified": True,
                    "is_active": True,
                    "is_platform_admin": False,
                },
            }
        ),
    }
    frontend = Path(__file__).resolve().parents[4] / "frontend"
    result = subprocess.run(
        [
            "npx.cmd",
            "--no-install",
            "playwright",
            "test",
            "--config=playwright.hr-live.config.ts",
        ],
        cwd=frontend,
        env=environment,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + result.stderr
