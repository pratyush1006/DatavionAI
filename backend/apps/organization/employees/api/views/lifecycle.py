"""
Employee lifecycle API views.

Workflow driven employee actions.

Supported:

- Activate employee
- Deactivate employee
- Change assignment
- Manage contract
- Employee onboarding
- Employee offboarding

Architecture:

API
 |
Serializer
 |
Workflow Request
 |
Workflow
 |
Service
 |
Domain Event
 |
Background Tasks
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.core.workflows import (
    WorkflowContext,
)
from apps.organization.employees.api.serializers import (
    EmployeeAssignmentActionSerializer,
    EmployeeContractActionSerializer,
    EmployeeOffboardingSerializer,
    EmployeeOnboardingSerializer,
    EmployeeStatusActionSerializer,
)
from apps.organization.employees.permissions import (
    CanActivateEmployee,
    CanAssignEmployee,
    CanDeactivateEmployee,
    CanManageEmployeeContracts,
    CanOffboardEmployee,
    CanOnboardEmployee,
)
from apps.organization.employees.workflows import (
    EmployeeActivationRequest,
    EmployeeActivationWorkflow,
    EmployeeAssignmentRequest,
    EmployeeAssignmentWorkflow,
    EmployeeContractManagementRequest,
    EmployeeContractManagementWorkflow,
    EmployeeDeactivationRequest,
    EmployeeDeactivationWorkflow,
    EmployeeOffboardingRequest,
    EmployeeOffboardingWorkflow,
    EmployeeOnboardingRequest,
    EmployeeOnboardingWorkflow,
)

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


def serialize_workflow_data(
    data: Any,
):
    """
    Convert workflow DTO output
    into API serializable payload.

    Supports:

    - dataclasses
    - DTO objects
    - primitive values
    """

    if data is None:
        return None

    if is_dataclass(
        data,
    ):
        return asdict(
            data,
        )

    if hasattr(
        data,
        "__dict__",
    ):
        return data.__dict__

    return data


# ============================================================
# Base Workflow API
# ============================================================


class EmployeeWorkflowAPIView(
    BaseGenericAPIView,
):
    """
    Base employee workflow action API.

    Provides:

    - Workflow execution
    - WorkflowContext creation
    - Standard API response

    Business logic remains inside workflows.
    """

    def build_workflow_context(
        self,
        *,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Build DatavionOS workflow context.

        Tenant resolution priority:

        1. Request tenant context
        2. Current organization tenant
        3. User organization role tenant
        """

        tenant = self.current_tenant

        if tenant is None:
            organization = getattr(
                self,
                "current_organization",
                None,
            )

            if organization is not None:
                tenant = organization.tenant

        if tenant is None:
            user = self.current_user

            organization_role = user.organization_roles.select_related(
                "organization__tenant",
            ).first()

            if organization_role:
                tenant = organization_role.organization.tenant

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required for employee lifecycle workflow.",
            )

        return WorkflowContext.create(
            tenant_id=tenant.id,
            actor_id=self.current_user.id,
            workflow_name=workflow_name,
            request_id=getattr(
                self.request,
                "request_id",
                None,
            ),
        )

    def execute_workflow(
        self,
        *,
        workflow,
        workflow_name: str,
    ):
        """
        Execute workflow and return
        JSON serializable response.
        """

        result = workflow.execute(
            context=self.build_workflow_context(
                workflow_name=workflow_name,
            ),
        )

        return self.success_response(
            data=serialize_workflow_data(
                result.data,
            ),
            message=result.message,
        )


# ============================================================
# Activate
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeActivateAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Activate employee.
    """

    permission_classes = (
        IsAuthenticated,
        CanActivateEmployee,
    )

    serializer_class = EmployeeStatusActionSerializer

    def post(
        self,
        request,
        employee_id,
    ):

        workflow = EmployeeActivationWorkflow(
            request=EmployeeActivationRequest(
                employee_id=employee_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.activate",
        )


# ============================================================
# Deactivate
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeDeactivateAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Deactivate employee.
    """

    permission_classes = (
        IsAuthenticated,
        CanDeactivateEmployee,
    )

    serializer_class = EmployeeStatusActionSerializer

    def post(
        self,
        request,
        employee_id,
    ):

        workflow = EmployeeDeactivationWorkflow(
            request=EmployeeDeactivationRequest(
                employee_id=employee_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.deactivate",
        )


# ============================================================
# Assignment
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeAssignmentAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Change employee assignment.
    """

    permission_classes = (
        IsAuthenticated,
        CanAssignEmployee,
    )

    serializer_class = EmployeeAssignmentActionSerializer

    def post(
        self,
        request,
        employee_id,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeAssignmentWorkflow(
            request=EmployeeAssignmentRequest(
                employee_id=employee_id,
                **serializer.validated_data,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.assignment",
        )


# ============================================================
# Contract
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeContractAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Manage employee contract.
    """

    permission_classes = (
        IsAuthenticated,
        CanManageEmployeeContracts,
    )

    serializer_class = EmployeeContractActionSerializer

    def post(
        self,
        request,
        employee_id,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeContractManagementWorkflow(
            request=(
                EmployeeContractManagementRequest(
                    employee_id=employee_id,
                    contract_data=(serializer.validated_data["contract_data"]),
                )
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.contract.manage",
        )


# ============================================================
# Onboarding
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeOnboardingAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Complete employee onboarding.
    """

    permission_classes = (
        IsAuthenticated,
        CanOnboardEmployee,
    )

    serializer_class = EmployeeOnboardingSerializer

    def post(
        self,
        request,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeOnboardingWorkflow(
            request=EmployeeOnboardingRequest(
                **serializer.validated_data,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.onboard",
        )


# ============================================================
# Offboarding
# ============================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeOffboardingAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Complete employee offboarding.
    """

    permission_classes = (
        IsAuthenticated,
        CanOffboardEmployee,
    )

    serializer_class = EmployeeOffboardingSerializer

    def post(
        self,
        request,
        employee_id,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeOffboardingWorkflow(
            request=EmployeeOffboardingRequest(
                employee_id=employee_id,
                **serializer.validated_data,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.offboard",
        )


__all__ = (
    "EmployeeActivateAPIView",
    "EmployeeDeactivateAPIView",
    "EmployeeAssignmentAPIView",
    "EmployeeContractAPIView",
    "EmployeeOnboardingAPIView",
    "EmployeeOffboardingAPIView",
)
