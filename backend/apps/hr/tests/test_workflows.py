"""Exercise HR API workflows and organization boundaries with real services."""

from datetime import date
from decimal import Decimal

import pytest
from django.urls import resolve
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.common.middleware.context import clear_context, set_current_organization
from apps.hr.leave.models import LeaveBalance
from apps.hr.onboarding.models import LifecycleTask
from apps.hr.payroll.models import Payslip
from apps.organization.employees.models import Employee
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization, OrganizationModule
from apps.platform.saas_billing.models import Plan, Subscription
from apps.platform.tenancy.models import Tenant


@pytest.fixture
def hr(db):
    tenant = Tenant.objects.create(
        name="HR", slug="hr-test", tenant_type="ORGANIZATION", status="ACTIVE"
    )
    organization = Organization.objects.create(
        tenant=tenant,
        name="HR",
        code="HR",
        slug="hr-test",
        organization_type="CLINIC",
        status="ACTIVE",
    )
    other = Organization.objects.create(
        tenant=tenant,
        name="Other",
        code="OTHER",
        slug="hr-other",
        organization_type="CLINIC",
        status="ACTIVE",
    )
    plan = Plan.objects.create(
        name="HR Test", code="hr-test", modules={"hr": True}, price=0
    )
    for selected in (organization, other):
        Subscription.objects.create(
            tenant=tenant,
            organization=selected,
            plan=plan,
            status="ACTIVE",
            plan_snapshot={"modules": {"hr": True}},
            feature_snapshot={"modules": {"hr": True}},
        )
        OrganizationModule.objects.create(
            organization=selected, module_code="hr", status="enabled"
        )
    admin = User.objects.create_superuser(
        email="hr-admin@test.com", password="test-password"
    )
    employee = Employee.objects.create(
        organization=organization,
        employee_code="HR001",
        designation="Nurse",
        joining_date=date(2026, 1, 1),
    )
    foreign_employee = Employee.objects.create(
        organization=other,
        employee_code="OTHER001",
        designation="Nurse",
        joining_date=date(2026, 1, 1),
    )
    factory = APIRequestFactory()

    def request(method, path, data=None, user=admin, selected=organization):
        set_current_organization(selected)
        http = getattr(factory, method)(
            f"/api/hr/{path}",
            data=data or {},
            format="json",
            HTTP_X_ORGANIZATION_ID=str(selected.pk),
        )
        http.organization = selected
        force_authenticate(http, user=user)
        match = resolve(f"/{path}", urlconf="apps.hr.schema_urls")
        return match.func(http, **match.kwargs)

    yield request, organization, employee, foreign_employee, other
    clear_context()


def created(response):
    assert response.status_code == 201, response.data
    return response.data["data"]["id"]


@pytest.mark.django_db
def test_attendance_crud_and_boundaries(hr):
    request, organization, employee, foreign_employee, other = hr
    record = created(
        request(
            "post",
            "attendance/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "work_date": "2026-01-10",
                "check_in": "09:00",
                "check_out": "17:00",
                "status": "present",
            },
        )
    )
    detail = request("get", f"attendance/{record}/")
    assert detail.data["data"]["employee_id"] == str(employee.pk)
    assert detail.data["data"]["organization_id"] == str(organization.pk)
    assert Decimal(detail.data["data"]["hours_worked"]) == 8
    assert (
        request("patch", f"attendance/{record}/", {"check_out": "18:00"}).status_code
        == 200
    )
    assert request("get", f"attendance/{record}/", selected=other).status_code == 404
    assert (
        request(
            "patch", f"attendance/{record}/", {"employee": str(foreign_employee.pk)}
        ).status_code
        == 400
    )
    assert (
        request("post", "attendance/", {"organization": str(other.pk)}).status_code
        == 400
    )
    outsider = User.objects.create_user(
        email="hr-outsider@test.com", password="test-password"
    )
    assert request("get", "attendance/", user=outsider).status_code == 403
    assert request("get", "attendance/").data["data"]
    assert request("delete", f"attendance/{record}/").status_code in (200, 204)


@pytest.mark.django_db
def test_leave_approval_and_cancellation_update_balance(hr):
    request, organization, employee, _, _ = hr
    leave_type = created(
        request(
            "post",
            "leave/types/",
            {"organization": str(organization.pk), "name": "Annual", "code": "ANNUAL"},
        )
    )
    created(
        request(
            "post",
            "leave/balances/",
            {
                "employee": str(employee.pk),
                "leave_type": leave_type,
                "year": 2026,
                "allocated_days": "20",
            },
        )
    )
    leave = created(
        request(
            "post",
            "leave/requests/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "leave_type": leave_type,
                "start_date": "2026-02-01",
                "end_date": "2026-02-02",
                "number_of_days": "2",
                "reason": "Vacation",
            },
        )
    )
    assert (
        request(
            "post", f"leave/requests/{leave}/approve/", {"decision_notes": "Approved"}
        ).status_code
        == 200
    )
    balance = LeaveBalance.objects.get(employee=employee)
    assert balance.used_days == 2
    assert request("post", f"leave/requests/{leave}/cancel/").status_code == 200
    balance.refresh_from_db()
    assert balance.used_days == 0
    leave2 = created(
        request(
            "post",
            "leave/requests/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "leave_type": leave_type,
                "start_date": "2026-03-01",
                "end_date": "2026-03-01",
                "number_of_days": "1",
            },
        )
    )
    assert request("post", f"leave/requests/{leave2}/approve/").status_code == 200
    assert request("delete", f"leave/requests/{leave2}/").status_code == 204
    balance.refresh_from_db()
    assert balance.used_days == 0


@pytest.mark.django_db
def test_payroll_totals_edit_process_and_pay(hr):
    request, organization, employee, _, _ = hr
    payslip = created(
        request(
            "post",
            "payroll/payslips/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "pay_period_start": "2026-01-01",
                "pay_period_end": "2026-01-31",
                "basic_salary": "1000",
                "total_allowances": "100",
                "currency": "INR",
                "line_items": [
                    {"component_type": "deduction", "name": "Tax", "amount": "50"}
                ],
            },
        )
    )
    instance = Payslip.objects.get(pk=payslip)
    assert instance.net_pay == Decimal("1050")
    assert (
        request(
            "patch", f"payroll/payslips/{payslip}/", {"basic_salary": "-1"}
        ).status_code
        == 400
    )
    assert (
        request(
            "patch",
            f"payroll/payslips/{payslip}/",
            {
                "line_items": [
                    {"component_type": "deduction", "name": "Excess", "amount": "2000"}
                ]
            },
        ).status_code
        == 400
    )
    assert (
        request(
            "patch", f"payroll/payslips/{payslip}/", {"basic_salary": "1200"}
        ).status_code
        == 200
    )
    instance.refresh_from_db()
    assert instance.net_pay == Decimal("1250")
    assert request("post", f"payroll/payslips/{payslip}/process/").status_code == 200
    assert request("post", f"payroll/payslips/{payslip}/mark-paid/").status_code == 200
    instance.refresh_from_db()
    assert instance.status == "paid"
    assert request("delete", f"payroll/payslips/{payslip}/").status_code == 400
    assert (
        request(
            "patch", f"payroll/payslips/{payslip}/", {"basic_salary": "2000"}
        ).status_code
        == 400
    )


@pytest.mark.django_db
def test_onboarding_templates_tasks_and_completion(hr):
    request, organization, employee, _, _ = hr
    created(
        request(
            "post",
            "onboarding/task-templates/",
            {
                "organization": str(organization.pk),
                "title": "Verify documents",
                "process_type": "onboarding",
                "is_mandatory": True,
            },
        )
    )
    process = created(
        request(
            "post",
            "onboarding/processes/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "process_type": "onboarding",
                "start_date": "2026-01-01",
            },
        )
    )
    task = LifecycleTask.objects.get(process_id=process)
    assert (
        request(
            "patch", f"onboarding/tasks/{task.pk}/", {"status": "completed"}
        ).status_code
        == 200
    )
    assert (
        request("post", f"onboarding/processes/{process}/complete/").status_code == 200
    )


@pytest.mark.django_db
def test_shifts_holidays_and_performance(hr):
    request, organization, employee, _, other = hr
    shift = created(
        request(
            "post",
            "shifts/",
            {
                "organization": str(organization.pk),
                "name": "Day",
                "code": "DAY",
                "start_time": "09:00",
                "end_time": "17:00",
            },
        )
    )
    created(
        request(
            "post",
            "shifts/assignments/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "shift": shift,
                "work_date": "2026-01-02",
            },
        )
    )
    holiday = created(
        request(
            "post",
            "holidays/",
            {
                "organization": str(organization.pk),
                "name": "Holiday",
                "date": "2026-01-03",
            },
        )
    )
    assert (
        request("post", f"holidays/{holiday}/apply-to-attendance/").status_code == 200
    )
    cycle = created(
        request(
            "post",
            "performance/cycles/",
            {
                "organization": str(organization.pk),
                "name": "Annual",
                "start_date": "2026-01-01",
                "end_date": "2026-12-31",
            },
        )
    )
    review = created(
        request(
            "post",
            "performance/reviews/",
            {"cycle": cycle, "employee": str(employee.pk), "overall_rating": "4.0"},
        )
    )
    goal = created(
        request("post", "performance/goals/", {"review": review, "title": "Training"})
    )
    assert (
        request("get", f"performance/goals/{goal}/", selected=other).status_code == 404
    )
    for action in ("submit", "acknowledge", "complete"):
        assert (
            request("post", f"performance/reviews/{review}/{action}/").status_code
            == 200
        )
