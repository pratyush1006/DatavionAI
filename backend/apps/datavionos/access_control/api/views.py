"""Organization access-control API views."""

from __future__ import annotations

from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.datavionos.access_control.api.serializers import (
    DepartmentMemberAssignmentSerializer,
    LifecycleSerializer,
    OrganizationDepartmentCreateSerializer,
    OrganizationMemberOnboardingSerializer,
    OrganizationRoleAssignmentSerializer,
    OrganizationTeamCreateSerializer,
)
from apps.datavionos.access_control.service import OrganizationAccessControlService
from apps.datavionos.selectors.bootstrap import PlatformBootstrapSelector
from apps.organization.departments.constants import DEFAULT_DEPARTMENT_TYPE
from apps.organization.departments.models import (
    Department,
    DepartmentMember,
    DepartmentRole,
)
from apps.organization.departments.services import DepartmentMemberService
from apps.organization.employees.models import Employee
from apps.organization.teams.models import Team, TeamDepartmentAssignment
from apps.platform.accounts.models import User
from apps.platform.rbac.constants import RoleScope, SystemRole
from apps.platform.rbac.engines.permission import user_has_permission
from apps.platform.rbac.models import OrganizationRole, Role
from apps.platform.rbac.services.organization_role import (
    activate_organization_role,
    create_organization_role,
    deactivate_organization_role,
    update_organization_role,
)


def can_create_departments(*, user, organization) -> bool:
    """Keep organization setup mutations behind the canonical permission gate."""
    return user_has_permission(
        user=user, permission="departments.create", organization=organization
    )


def resolve_active_organization(*, user):
    """Resolve the active organization through canonical bootstrap.

    Platform administrators may operate an organization without holding an
    organization-role row.  Their selected/default organization on the user
    record remains a valid server-side context; without this fallback the
    access-control screen incorrectly returned 404 for platform operators.
    """
    bootstrap = PlatformBootstrapSelector().get(user=user)
    organization = bootstrap.organization or getattr(user, "organization", None)
    if organization is None or not organization.is_active:
        from rest_framework.exceptions import NotFound

        raise NotFound("Active organization context was not found.")
    return organization


def forbidden(detail: str) -> Response:
    return Response({"detail": detail}, status=status.HTTP_403_FORBIDDEN)


class OrganizationAccessControlAPIView(APIView):
    """Return organization departments, users, roles and permissions."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization = resolve_active_organization(user=request.user)
        allowed = (
            user_has_permission(
                user=request.user, permission="rbac.view", organization=organization
            )
            or user_has_permission(
                user=request.user, permission="rbac.assign", organization=organization
            )
            or user_has_permission(
                user=request.user,
                permission="employees.create",
                organization=organization,
            )
        )
        if not allowed:
            return forbidden("You do not have permission to view access controls.")
        snapshot = OrganizationAccessControlService().resolve(
            user=request.user, organization=organization
        )
        return success_response(
            data={
                "organization": snapshot.organization,
                "departments": snapshot.departments,
                "teams": snapshot.teams,
                "department_type_options": snapshot.department_type_options,
                "department_templates": snapshot.department_templates,
                "team_type_options": snapshot.team_type_options,
                "team_templates": snapshot.team_templates,
                "organization_roles": snapshot.organization_roles,
                "available_roles": snapshot.available_roles,
                "employees": snapshot.employees,
                "department_memberships": snapshot.department_memberships,
                "permissions": snapshot.permissions,
                "ai_capabilities": snapshot.ai_capabilities,
                "can_manage_access": snapshot.can_manage_access,
                "can_manage_departments": snapshot.can_manage_departments,
            }
        )


class OrganizationDepartmentCreateAPIView(APIView):
    """Create a department in active context without exposing organization IDs."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        organization = resolve_active_organization(user=request.user)
        if not can_create_departments(user=request.user, organization=organization):
            return forbidden("You do not have permission to create departments.")

        serializer = OrganizationDepartmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        from apps.core.workflows import WorkflowContext
        from apps.organization.departments.workflows import (
            DepartmentCreationRequest,
            DepartmentCreationWorkflow,
        )

        with transaction.atomic():
            result = DepartmentCreationWorkflow(
                request=DepartmentCreationRequest(
                    organization_id=organization.id,
                    name=payload["name"].strip(),
                    code=payload["code"].strip().upper(),
                    department_type=payload.get(
                        "department_type", DEFAULT_DEPARTMENT_TYPE
                    ),
                )
            ).execute(
                context=WorkflowContext(
                    tenant_id=organization.tenant_id,
                    actor_id=request.user.id,
                    request_id=request.headers.get("X-Request-ID"),
                    workflow_name="organization.department_create",
                )
            )
            if not result.success or result.data is None:
                raise ValidationError(
                    {"detail": result.message or "Department could not be created."}
                )
            department = Department.objects.get(pk=result.data.department_id)

        return success_response(
            data={
                "id": str(department.pk),
                "name": department.name,
                "code": department.code,
            },
            message="Department created successfully.",
            request=request,
            status_code=status.HTTP_201_CREATED,
        )


class OrganizationTeamCreateAPIView(APIView):
    """Create a team and its required department assignment atomically."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        organization = resolve_active_organization(user=request.user)
        if not can_create_departments(user=request.user, organization=organization):
            return forbidden("You do not have permission to create teams.")

        serializer = OrganizationTeamCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        department = get_object_or_404(
            Department,
            pk=payload["department_id"],
            organization=organization,
        )

        from apps.core.workflows import WorkflowContext
        from apps.organization.teams.workflows import (
            TeamCreationRequest,
            TeamCreationWorkflow,
        )

        with transaction.atomic():
            result = TeamCreationWorkflow(
                request=TeamCreationRequest(
                    organization_id=organization.id,
                    name=payload["name"].strip(),
                    code=payload["code"].strip().upper(),
                    team_type=payload.get("team_type") or None,
                )
            ).execute(
                context=WorkflowContext(
                    tenant_id=organization.tenant_id,
                    actor_id=request.user.id,
                    request_id=request.headers.get("X-Request-ID"),
                    workflow_name="organization.team_create",
                )
            )
            if not result.success or result.data is None:
                raise ValidationError(
                    {"detail": result.message or "Team could not be created."}
                )
            team = Team.objects.get(pk=result.data.team_id, organization=organization)
            TeamDepartmentAssignment.objects.create(
                team=team,
                department=department,
                is_primary=True,
                is_active=True,
            )

        return success_response(
            data={
                "id": str(team.pk),
                "name": team.name,
                "code": team.code,
                "department_id": str(department.pk),
            },
            message="Team created successfully.",
            request=request,
            status_code=status.HTTP_201_CREATED,
        )


class OrganizationRoleAssignmentAPIView(APIView):
    """Assign or update an organization-scoped RBAC role."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        organization = resolve_active_organization(user=request.user)
        if not user_has_permission(
            user=request.user, permission="rbac.assign", organization=organization
        ):
            return forbidden("You do not have permission to assign organization roles.")

        serializer = OrganizationRoleAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user = get_object_or_404(User, pk=serializer.validated_data["user_id"])
        role = get_object_or_404(
            Role,
            pk=serializer.validated_data["role_id"],
            is_active=True,
            is_assignable=True,
            scope=RoleScope.ORGANIZATION,
        ).exclude(
            code__in=(
                SystemRole.PLATFORM_ADMIN,
                SystemRole.ORGANIZATION_OWNER,
                SystemRole.ORGANIZATION_ADMIN,
            )
        )

        # The assignment itself is always routed through the canonical RBAC service.
        assignment, created = OrganizationRole.objects.get_or_create(
            organization=organization,
            user=target_user,
            role=role,
            defaults={
                "is_primary": serializer.validated_data["is_primary"],
                "is_active": serializer.validated_data["is_active"],
            },
        )
        if created:
            assignment.delete()
            assignment = create_organization_role(
                validated_data={
                    "organization": organization,
                    "user": target_user,
                    "role": role,
                    "is_primary": serializer.validated_data["is_primary"],
                    "is_active": serializer.validated_data["is_active"],
                }
            )
        else:
            assignment = update_organization_role(
                instance=assignment,
                validated_data={
                    "is_primary": serializer.validated_data["is_primary"],
                    "is_active": serializer.validated_data["is_active"],
                },
            )

        return Response(
            {
                "id": str(assignment.pk),
                "user_id": str(assignment.user_id),
                "role_id": str(assignment.role_id),
                "is_primary": assignment.is_primary,
                "is_active": assignment.is_active,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class OrganizationMemberOnboardingAPIView(APIView):
    """Create a login-enabled employee and assign one organization role."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        organization = resolve_active_organization(user=request.user)
        # HR can complete a hire (login, employee record and a standard
        # organization role) without receiving the far broader ability to
        # administer existing role assignments.  Platform, owner and
        # organization-admin roles remain excluded below.
        can_manage_members = user_has_permission(
            user=request.user, permission="employees.create", organization=organization
        )
        if not can_manage_members:
            return forbidden(
                "You do not have permission to onboard organization members."
            )

        serializer = OrganizationMemberOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        role = get_object_or_404(
            Role,
            pk=payload["role_id"],
            is_active=True,
            is_system=True,
            is_assignable=True,
            scope=RoleScope.ORGANIZATION,
        ).exclude(
            code__in=(
                SystemRole.PLATFORM_ADMIN,
                SystemRole.ORGANIZATION_OWNER,
                SystemRole.ORGANIZATION_ADMIN,
            )
        )

        from uuid import uuid4

        from apps.core.workflows import WorkflowContext
        from apps.organization.employees.workflows import (
            EmployeeOnboardingRequest,
            EmployeeOnboardingWorkflow,
        )

        with transaction.atomic():
            user = User.objects.create_user(
                email=payload["email"],
                first_name=payload["first_name"].strip(),
                last_name=payload["last_name"].strip(),
                phone=payload.get("phone", "").strip(),
                organization=organization,
                password=payload["temporary_password"],
            )
            employee_code = payload.get("employee_code", "").strip().upper()
            if not employee_code:
                employee_code = f"EMP-{uuid4().hex[:8].upper()}"

            workflow = EmployeeOnboardingWorkflow(
                request=EmployeeOnboardingRequest(
                    organization_id=organization.id,
                    employee_data={
                        "user_id": user.id,
                        "employee_code": employee_code,
                        "designation": payload["designation"].strip(),
                        "work_email": user.email,
                        "phone_number": user.phone,
                        "employment_type": payload["employment_type"],
                        "joining_date": payload["joining_date"],
                    },
                    assignment_data=(
                        {
                            "department_id": payload["department_id"],
                            "team_id": payload.get("team_id"),
                            "supervisor_id": payload.get("supervisor_id"),
                        }
                        if payload.get("department_id")
                        else None
                    ),
                )
            )
            result = workflow.execute(
                context=WorkflowContext(
                    tenant_id=organization.tenant_id,
                    actor_id=request.user.id,
                    request_id=request.headers.get("X-Request-ID"),
                    workflow_name="organization.member_onboard",
                )
            )
            if not result.success or result.data is None:
                transaction.set_rollback(True)
                raise ValidationError(
                    {
                        "detail": result.message
                        or "Employee onboarding could not be completed."
                    }
                )

            assignment = create_organization_role(
                validated_data={
                    "organization": organization,
                    "user": user,
                    "role": role,
                    "is_primary": True,
                    "is_active": True,
                }
            )

        return Response(
            {
                "user_id": str(user.id),
                "employee_id": str(result.data.employee_id),
                "role_assignment_id": str(assignment.id),
                "role_name": role.name,
            },
            status=status.HTTP_201_CREATED,
        )


class OrganizationRoleLifecycleAPIView(APIView):
    """Activate or deactivate an organization role assignment."""

    permission_classes = (IsAuthenticated,)

    def patch(self, request, assignment_id: UUID):
        organization = resolve_active_organization(user=request.user)
        if not user_has_permission(
            user=request.user, permission="rbac.assign", organization=organization
        ):
            return forbidden("You do not have permission to manage organization roles.")
        assignment = get_object_or_404(
            OrganizationRole, pk=assignment_id, organization=organization
        )
        serializer = LifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment = (
            activate_organization_role(instance=assignment)
            if serializer.validated_data["is_active"]
            else deactivate_organization_role(instance=assignment)
        )
        return Response({"id": str(assignment.pk), "is_active": assignment.is_active})


class DepartmentMemberAssignmentAPIView(APIView):
    """Assign an employee to a department using the domain service."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        organization = resolve_active_organization(user=request.user)
        if not user_has_permission(
            user=request.user,
            permission="departments.update",
            organization=organization,
        ):
            return forbidden(
                "You do not have permission to manage department membership."
            )

        serializer = DepartmentMemberAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = get_object_or_404(
            Department,
            pk=serializer.validated_data["department_id"],
            organization=organization,
        )
        employee = get_object_or_404(
            Employee,
            pk=serializer.validated_data["employee_id"],
            organization=organization,
        )
        role = None
        if serializer.validated_data.get("role_id"):
            role = get_object_or_404(
                DepartmentRole,
                pk=serializer.validated_data["role_id"],
                department=department,
            )
        member = DepartmentMemberService.assign(
            department=department,
            employee=employee,
            role=role,
            title=serializer.validated_data.get("title", ""),
            is_primary=serializer.validated_data.get("is_primary", False),
        )
        return Response(
            {
                "id": str(member.pk),
                "department_id": str(member.department_id),
                "employee_id": str(member.employee_id),
                "role_id": str(member.role_id) if member.role_id else None,
                "is_primary": member.is_primary,
                "is_active": member.is_active,
            },
            status=status.HTTP_201_CREATED,
        )


class DepartmentMemberLifecycleAPIView(APIView):
    """Activate or deactivate a department membership."""

    permission_classes = (IsAuthenticated,)

    def patch(self, request, membership_id: UUID):
        organization = resolve_active_organization(user=request.user)
        if not user_has_permission(
            user=request.user,
            permission="departments.update",
            organization=organization,
        ):
            return forbidden(
                "You do not have permission to manage department membership."
            )
        serializer = LifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = get_object_or_404(
            DepartmentMember,
            pk=membership_id,
            department__organization=organization,
        )
        if serializer.validated_data["is_active"]:
            member.is_active = True
            member.save(update_fields=["is_active"])
        else:
            DepartmentMemberService.deactivate(instance=member)
        return Response({"id": str(member.pk), "is_active": member.is_active})
