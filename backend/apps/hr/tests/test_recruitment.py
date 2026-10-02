"""Recruitment lifecycle and seeded role authorization using real API services."""

from uuid import uuid4

import pytest

from apps.hr.tests.test_workflows import created
from apps.platform.accounts.models import User
from apps.platform.organizations.models import OrganizationModule
from apps.platform.rbac.constants import SystemRole
from apps.platform.rbac.models import OrganizationRole, Permission, Role, RolePermission
from apps.platform.rbac.seed_data.permissions import PERMISSIONS
from apps.platform.rbac.seed_data.role_permissions import SYSTEM_ROLE_PERMISSIONS
from apps.platform.saas_billing.models import Subscription


def assign_hr_role(organization, code):
    user = User.objects.create_user(
        email=f"{code}-{uuid4().hex}@test.com", password="test-password"
    )
    role, _ = Role.objects.get_or_create(
        code=code, defaults={"name": code, "scope": "organization"}
    )
    codes = set(SYSTEM_ROLE_PERMISSIONS[code])
    for values in PERMISSIONS:
        if values["code"] in codes:
            permission, _ = Permission.objects.get_or_create(
                code=values["code"], defaults=values
            )
            RolePermission.objects.get_or_create(role=role, permission=permission)
    OrganizationRole.objects.create(user=user, role=role, organization=organization)
    return user


@pytest.mark.django_db
def test_hr_endpoints_respect_subscription_and_organization_enablement(hr):
    request, organization, employee, foreign_employee, other = hr
    module = OrganizationModule.objects.get(organization=organization, module_code="hr")
    module.status = "disabled"
    module.save()
    assert request("get", "attendance/").status_code == 403
    module.status = "enabled"
    module.save()
    subscription = Subscription.objects.get(organization=organization)
    subscription.status = "CANCELLED"
    subscription.save()
    assert request("get", "recruitment/jobs/").status_code == 403


@pytest.mark.django_db
def test_recruitment_lifecycle_and_boundaries(hr):
    request, organization, employee, foreign_employee, other = hr
    job = created(
        request(
            "post",
            "recruitment/jobs/",
            {
                "organization": str(organization.pk),
                "title": "Nurse",
                "status": "open",
                "vacancies": 2,
            },
        )
    )
    candidate = created(
        request(
            "post",
            "recruitment/candidates/",
            {
                "organization": str(organization.pk),
                "job": job,
                "full_name": "New Nurse",
                "email": "new@test.com",
            },
        )
    )
    assert (
        request(
            "patch", f"recruitment/candidates/{candidate}/", {"status": "hired"}
        ).status_code
        == 400
    )
    assert (
        request(
            "patch", f"recruitment/candidates/{candidate}/", {"status": "shortlisted"}
        ).status_code
        == 200
    )
    payload = {
        "organization": str(organization.pk),
        "candidate": candidate,
        "interviewer": str(employee.pk),
        "scheduled_at": "2026-10-02T09:00:00Z",
    }
    assert (
        request(
            "post",
            "recruitment/interviews/",
            {**payload, "interviewer": str(foreign_employee.pk)},
        ).status_code
        == 400
    )
    interview = created(request("post", "recruitment/interviews/", payload))
    assert (
        request("get", f"recruitment/candidates/{candidate}/").data["data"]["status"]
        == "interviewing"
    )
    assert (
        request(
            "post",
            "recruitment/interviews/",
            {**payload, "scheduled_at": "2026-10-02T09:30:00Z"},
        ).status_code
        == 400
    )
    assert (
        request(
            "patch", f"recruitment/interviews/{interview}/", {"status": "completed"}
        ).status_code
        == 400
    )
    assert (
        request(
            "patch",
            f"recruitment/interviews/{interview}/",
            {"status": "completed", "feedback": "Suitable candidate"},
        ).status_code
        == 200
    )
    assert (
        request(
            "patch", f"recruitment/candidates/{candidate}/", {"status": "offered"}
        ).status_code
        == 200
    )
    hired = request(
        "patch",
        f"recruitment/candidates/{candidate}/",
        {"status": "hired", "employee_code": "NEW001", "joining_date": "2026-10-03"},
    )
    assert hired.status_code == 200, hired.data
    assert hired.data["data"]["hired_employee"]
    from apps.hr.onboarding.models import LifecycleProcess

    assert LifecycleProcess.objects.filter(
        employee_id=hired.data["data"]["hired_employee"], process_type="onboarding"
    ).exists()
    assert request("delete", f"recruitment/jobs/{job}/").status_code == 400
    assert request("get", f"recruitment/jobs/{job}/", selected=other).status_code == 404
    assert (
        request(
            "get", f"recruitment/candidates/{candidate}/", selected=other
        ).status_code
        == 404
    )
    assert (
        request(
            "get", f"recruitment/interviews/{interview}/", selected=other
        ).status_code
        == 404
    )
    assert (
        request("patch", f"recruitment/jobs/{job}/", {"status": "closed"}).status_code
        == 200
    )
    assert (
        request(
            "post",
            "recruitment/candidates/",
            {
                "organization": str(organization.pk),
                "job": job,
                "full_name": "Other",
                "email": "other@test.com",
            },
        ).status_code
        == 400
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "code", [SystemRole.HR_MANAGER.value, SystemRole.HR_EXECUTIVE.value]
)
def test_seeded_hr_roles_can_use_workflows_without_superuser(hr, code):
    request, organization, employee, foreign_employee, other = hr
    user = assign_hr_role(organization, code)
    from apps.platform.rbac.engines import user_has_permission

    assert user_has_permission(
        user=user, permission="departments.view", organization=organization
    )
    for path in (
        "attendance/",
        "leave/requests/",
        "shifts/",
        "holidays/",
        "onboarding/processes/",
        "payroll/payslips/",
        "performance/reviews/",
        "recruitment/jobs/",
    ):
        response = request("get", path, user=user)
        assert response.status_code == 200, (path, response.data)
        assert request("get", path, user=user, selected=other).status_code == 403
    record = created(
        request(
            "post",
            "attendance/",
            {
                "organization": str(organization.pk),
                "employee": str(employee.pk),
                "work_date": "2026-10-01",
                "status": "present",
            },
            user=user,
        )
    )
    assert request("delete", f"attendance/{record}/", user=user).status_code == (
        204 if code == "hr_manager" else 403
    )
