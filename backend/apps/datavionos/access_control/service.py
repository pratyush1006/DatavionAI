"""Application service for organization context and RBAC administration."""

from __future__ import annotations

from apps.organization.departments.constants import DepartmentType
from apps.organization.departments.models import Department, DepartmentMember
from apps.organization.employees.models import Employee
from apps.organization.teams.models import TeamDepartmentAssignment
from apps.platform.rbac.constants import RoleScope, SystemRole
from apps.platform.rbac.engines.permission import user_has_permission
from apps.platform.rbac.models import OrganizationRole, Role

# Team.type is currently a free-text domain field.  Keep the operational
# vocabulary on the backend so clients do not hard-code independent lists.
TEAM_TYPE_OPTIONS = (
    ("CLINICAL", "Clinical"),
    ("NURSING", "Nursing"),
    ("OPERATIONS", "Operations"),
    ("ADMINISTRATION", "Administration"),
    ("BILLING", "Billing"),
    ("SUPPORT", "Support"),
)

TEAM_TEMPLATE_DEFINITIONS = (
    ("CLINICAL", "Clinical Care Team", "CLIN"),
    ("NURSING", "Nursing Care Team", "NURS"),
    ("OPERATIONS", "Operations Team", "OPS"),
    ("ADMINISTRATION", "Administration Team", "ADMIN"),
    ("BILLING", "Billing Team", "BILL"),
    ("SUPPORT", "Support Team", "SUP"),
)

# Canonical organization-setup catalogue.  The UI receives this from the
# backend and cannot pair a department name with an unrelated code or type.
DEPARTMENT_TEMPLATES = (
    ("GENERAL", "General Services", "GENERAL"),
    ("CLINICAL", "Cardiology", "CARD"),
    ("CLINICAL", "Neurology", "NEUR"),
    ("CLINICAL", "Orthopedics", "ORTHO"),
    ("CLINICAL", "Pediatrics", "PEDS"),
    ("CLINICAL", "Gynecology", "GYN"),
    ("CLINICAL", "Dermatology", "DERM"),
    ("CLINICAL", "Oncology", "ONCO"),
    ("EMERGENCY", "Emergency Department", "ED"),
    ("OUTPATIENT", "Outpatient Department", "OPD"),
    ("INPATIENT", "Inpatient Department", "IPD"),
    ("ICU", "Intensive Care Unit", "ICU"),
    ("OPERATION_THEATRE", "Operation Theatre", "OT"),
    ("LABORATORY", "Laboratory", "LAB"),
    ("RADIOLOGY", "Radiology", "RAD"),
    ("PHARMACY", "Pharmacy", "PHARM"),
    ("BLOOD_BANK", "Blood Bank", "BB"),
    ("REHABILITATION", "Rehabilitation", "REHAB"),
    ("BILLING", "Billing", "BILL"),
    ("FINANCE", "Finance", "FIN"),
    ("HUMAN_RESOURCES", "Human Resources", "HR"),
    ("INFORMATION_TECHNOLOGY", "Information Technology", "IT"),
    ("MEDICAL_RECORDS", "Medical Records", "MRD"),
    ("HOUSEKEEPING", "Housekeeping", "HK"),
    ("SECURITY", "Security", "SEC"),
    ("PROCUREMENT", "Procurement", "PROC"),
    ("BIOMEDICAL", "Biomedical Engineering", "BIOMED"),
    ("NURSING", "Nursing", "NURS"),
    ("TELEMEDICINE", "Telemedicine", "TELE"),
    ("RESEARCH", "Research", "RES"),
    ("QUALITY", "Quality", "QA"),
    ("OTHER", "Other Services", "OTHER"),
)


class OrganizationAccessControlService:
    """Resolve organization access state without replacing domain authorities."""

    @staticmethod
    def employee_name(employee: Employee) -> str:
        user = getattr(employee, "user", None)
        first = str(getattr(user, "first_name", "") or "").strip()
        last = str(getattr(user, "last_name", "") or "").strip()
        name = " ".join(x for x in (first, last) if x)
        return name or str(getattr(employee, "employee_code", "") or employee.pk)

    def resolve(self, *, user, organization):
        from apps.datavionos.access_control.contracts import OrganizationAccessSnapshot

        can_manage_access = user_has_permission(
            user=user, permission="rbac.assign", organization=organization
        )
        can_manage_departments = user_has_permission(
            user=user, permission="departments.update", organization=organization
        ) or user_has_permission(
            user=user, permission="departments.create", organization=organization
        )

        departments = list(
            Department.objects.filter(organization=organization).order_by("name")
        )
        team_assignments = (
            TeamDepartmentAssignment.objects.filter(
                team__organization=organization,
                team__is_active=True,
                is_active=True,
            )
            .select_related("team", "department")
            .order_by("team__name", "department__name")
        )
        employees = (
            Employee.objects.filter(organization=organization)
            .select_related("user")
            .order_by("id")
        )
        organization_roles = (
            OrganizationRole.objects.filter(organization=organization)
            .select_related("user", "role")
            .order_by("user_id", "role__display_order", "role__name")
        )
        # Never expose platform roles in an organization's role picker.  An
        # organization administrator may grant only organization-scoped roles.
        available_roles = (
            Role.objects.filter(
                is_active=True,
                is_system=True,
                is_assignable=True,
                scope=RoleScope.ORGANIZATION,
            )
            .exclude(
                code__in=(
                    SystemRole.PLATFORM_ADMIN,
                    SystemRole.ORGANIZATION_OWNER,
                    SystemRole.ORGANIZATION_ADMIN,
                )
            )
            .order_by("display_order", "name")
        )
        memberships = (
            DepartmentMember.objects.filter(department__organization=organization)
            .select_related("department", "employee", "role")
            .order_by("department__name", "employee_id")
        )
        return OrganizationAccessSnapshot(
            organization={
                "id": str(organization.pk),
                "name": organization.name,
                "code": organization.code,
                "organization_type": getattr(organization, "organization_type", None),
            },
            departments=[
                {
                    "id": str(x.pk),
                    "name": x.name,
                    "code": x.code,
                    "slug": getattr(x, "slug", None),
                    "department_type": getattr(x, "department_type", None),
                    "status": getattr(x, "status", None),
                    "is_active": bool(getattr(x, "is_active", True)),
                    "parent_id": (
                        str(x.parent_id) if getattr(x, "parent_id", None) else None
                    ),
                }
                for x in departments
            ],
            teams=[
                {
                    "id": str(x.team_id),
                    "name": x.team.name,
                    "code": x.team.code,
                    "department_id": str(x.department_id),
                }
                for x in team_assignments
            ],
            department_type_options=[
                {"value": value, "label": label}
                for value, label in DepartmentType.choices
            ],
            department_templates=[
                {"department_type": department_type, "name": name, "code": code}
                for department_type, name, code in DEPARTMENT_TEMPLATES
            ],
            team_type_options=[
                {"value": value, "label": label} for value, label in TEAM_TYPE_OPTIONS
            ],
            team_templates=[
                {
                    "department_id": str(department.pk),
                    "team_type": team_type,
                    "name": f"{department.name} {name}",
                    "code": f"{department.code}-{code}",
                }
                for department in departments
                for team_type, name, code in TEAM_TEMPLATE_DEFINITIONS
            ],
            organization_roles=[
                {
                    "id": str(x.pk),
                    "user_id": str(x.user_id),
                    "user_email": getattr(x.user, "email", ""),
                    "user_name": (
                        " ".join(
                            p
                            for p in (
                                getattr(x.user, "first_name", ""),
                                getattr(x.user, "last_name", ""),
                            )
                            if p
                        )
                        or getattr(x.user, "email", "")
                    ),
                    "role_id": str(x.role_id),
                    "role_code": x.role.code,
                    "role_name": x.role.name,
                    "role_scope": x.role.scope,
                    "role_type": x.role.role_type,
                    "is_primary": x.is_primary,
                    "is_active": x.is_active,
                }
                for x in organization_roles
            ],
            available_roles=[
                {
                    "id": str(x.pk),
                    "code": x.code,
                    "name": x.name,
                    "description": x.description,
                    "role_type": x.role_type,
                    "scope": x.scope,
                    "category": x.category,
                    "priority": x.priority,
                    "is_system": x.is_system,
                    "is_default": x.is_default,
                    "is_active": x.is_active,
                }
                for x in available_roles
            ],
            employees=[
                {
                    "id": str(x.pk),
                    "user_id": str(x.user_id) if x.user_id else None,
                    "name": self.employee_name(x),
                    "email": getattr(getattr(x, "user", None), "email", ""),
                    "code": getattr(x, "employee_code", None),
                    "is_active": bool(getattr(x, "is_active", True)),
                }
                for x in employees
            ],
            department_memberships=[
                {
                    "id": str(x.pk),
                    "department_id": str(x.department_id),
                    "department_name": x.department.name,
                    "employee_id": str(x.employee_id),
                    "employee_name": self.employee_name(x.employee),
                    "role_id": str(x.role_id) if x.role_id else None,
                    "role_code": getattr(x.role, "code", None),
                    "role_name": getattr(x.role, "name", None),
                    "title": x.title,
                    "is_primary": x.is_primary,
                    "is_active": x.is_active,
                }
                for x in memberships
            ],
            # Permission catalogues are platform-wide and were being loaded on
            # every access-control request even though this organization screen
            # does not render or mutate individual permissions.  Role
            # assignment remains backend-authoritative; omit the unused,
            # potentially large catalogue from this organization snapshot.
            permissions=[],
            # AI capability data is not owned by the access-control snapshot.
            # The former generated ``.builder()`` call does not exist on the
            # immutable context and caused every access-control request to
            # fail with HTTP 500.
            ai_capabilities={},
            can_manage_access=can_manage_access,
            can_manage_departments=can_manage_departments,
        )
