"""
Employee lifecycle API views.

Workflow-driven employee lifecycle actions.

Responsibilities
----------------
- Authentication
- Permission declarations
- Request validation
- Workflow request construction
- Workflow execution
- Standard API response serialization

Business rules remain inside workflow and domain-service layers.

Architecture
------------

API
 |
 v
Serializer
 |
 v
Workflow Request
 |
 v
Workflow
 |
 v
Domain Service
 |
 v
Domain Event
 |
 v
Background Tasks
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Final

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import (
    error_response,
)
from apps.common.exceptions.codes import (
    ErrorCode,
)
from apps.core.workflows import (
    WorkflowContext,
    WorkflowResult,
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
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

EMPLOYEE_TAG: Final[tuple[str, ...]] = ("Employees",)


# =============================================================================
# Serialization
# =============================================================================


def serialize_workflow_data(
    data: Any,
) -> Any:
    """
    Convert workflow DTO output into API-safe structured data.

    Supports:

    - dataclasses
    - objects exposing to_dict()
    - objects exposing __dict__
    - primitive values
    - None
    """

    if data is None:
        return None

    if is_dataclass(data):
        return asdict(data)

    to_dict = getattr(
        data,
        "to_dict",
        None,
    )

    if callable(to_dict):
        return to_dict()

    if hasattr(
        data,
        "__dict__",
    ):
        return dict(data.__dict__)

    return data


# =============================================================================
# Error Mapping
# =============================================================================


def _resolve_error_code(
    code: str | None,
) -> ErrorCode:
    """
    Resolve a workflow error code into the platform ErrorCode enum.

    Workflow codes are intentionally allowed to remain domain-specific.
    When a workflow code does not have a corresponding platform-level
    ErrorCode, validation error is used as the safe standardized fallback.
    """

    if not code:
        return ErrorCode.VALIDATION_ERROR

    #
    # Match enum values first.
    #
    for error_code in ErrorCode:
        if error_code.value == code:
            return error_code

    #
    # Match enum member names.
    #
    normalized = code.upper()

    member = ErrorCode.__members__.get(
        normalized,
    )

    if member is not None:
        return member

    return ErrorCode.VALIDATION_ERROR


def _workflow_error_status(
    *,
    result: WorkflowResult[Any],
) -> int:
    """
    Resolve an appropriate HTTP status for a failed workflow.

    Workflow/domain error codes remain the primary source of semantic
    information. This function only translates those semantics into HTTP.
    """

    code = (result.code or "").lower()

    message = (result.message or "").lower()

    combined = f"{code} {message}"

    if any(
        value in combined
        for value in (
            "permission",
            "forbidden",
            "not_allowed",
            "unauthorized",
        )
    ):
        return status.HTTP_403_FORBIDDEN

    if any(
        value in combined
        for value in (
            "not_found",
            "does_not_exist",
            "not found",
        )
    ):
        return status.HTTP_404_NOT_FOUND

    if any(
        value in combined
        for value in (
            "conflict",
            "already_exists",
            "already exists",
            "duplicate",
        )
    ):
        return status.HTTP_409_CONFLICT

    return status.HTTP_400_BAD_REQUEST


def _workflow_error_details(
    result: WorkflowResult[Any],
) -> Any:
    """
    Serialize workflow error details when available.
    """

    if result.error is None:
        return None

    to_dict = getattr(
        result.error,
        "to_dict",
        None,
    )

    if callable(to_dict):
        return to_dict()

    details = getattr(
        result.error,
        "details",
        None,
    )

    if details is not None:
        return details

    return None


# =============================================================================
# Base Workflow API
# =============================================================================


class EmployeeWorkflowAPIView(
    BaseGenericAPIView,
):
    """
    Base API view for employee lifecycle workflows.

    Responsibilities:

    - Resolve tenant context
    - Build workflow context
    - Execute workflow
    - Preserve workflow success/failure state
    - Serialize standardized API responses
    """

    def build_workflow_context(
        self,
        *,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Build a DatavionOS workflow context.

        Tenant resolution priority:

        1. Request tenant context
        2. Current organization tenant
        3. User organization-role tenant
        """

        tenant = self.current_tenant

        if tenant is None:
            organization = self.current_organization

            if organization is not None:
                tenant = getattr(
                    organization,
                    "tenant",
                    None,
                )

        if tenant is None:
            user = self.current_user

            organization_roles = getattr(
                user,
                "organization_roles",
                None,
            )

            if organization_roles is not None:
                organization_role = organization_roles.select_related(
                    "organization__tenant",
                ).first()

                if organization_role is not None:
                    tenant = organization_role.organization.tenant

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required for employee lifecycle workflow.",
            )

        actor_id = getattr(
            self.current_user,
            "id",
            None,
        )

        if actor_id is None:
            raise RuntimeError(
                "Authenticated actor is required for employee lifecycle workflow.",
            )

        return WorkflowContext.create(
            tenant_id=tenant.id,
            actor_id=actor_id,
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
        workflow: Any,
        workflow_name: str,
    ):
        """
        Execute an employee workflow and preserve its outcome.

        Successful workflows return the standard success envelope.

        Failed workflows return the standard error envelope instead of
        incorrectly converting failures into HTTP 200 success responses.
        """

        result = workflow.execute(
            context=self.build_workflow_context(
                workflow_name=workflow_name,
            ),
        )

        if not result.success:
            return error_response(
                code=_resolve_error_code(
                    result.code,
                ),
                message=(result.message or "Workflow execution failed."),
                details=_workflow_error_details(
                    result,
                ),
                meta={
                    "workflow": workflow_name,
                    "workflow_code": (result.code),
                },
                request=self.request,
                status_code=_workflow_error_status(
                    result=result,
                ),
            )

        return self.success_response(
            data=serialize_workflow_data(
                result.data,
            ),
            message=result.message,
            meta={
                "workflow": workflow_name,
                "workflow_code": (result.code),
            },
        )


# =============================================================================
# Activate
# =============================================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeActivateAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Activate an employee.
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
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeActivationWorkflow(
            request=EmployeeActivationRequest(
                employee_id=employee_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.activate",
        )


# =============================================================================
# Deactivate
# =============================================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeDeactivateAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Deactivate an employee.
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
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = EmployeeDeactivationWorkflow(
            request=EmployeeDeactivationRequest(
                employee_id=employee_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.deactivate",
        )


# =============================================================================
# Assignment
# =============================================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeAssignmentAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Change an employee's organizational assignment.
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


# =============================================================================
# Contract
# =============================================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeContractAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Create an employee contract.
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
            request=EmployeeContractManagementRequest(
                employee_id=employee_id,
                contract_data=dict(
                    serializer.validated_data,
                ),
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.contract.manage",
        )


# =============================================================================
# Onboarding
# =============================================================================


@extend_schema(
    tags=EMPLOYEE_TAG,
)
class EmployeeOnboardingAPIView(
    EmployeeWorkflowAPIView,
):
    """
    Complete employee onboarding.

    The onboarding workflow orchestrates:

    - Employee creation
    - Optional contract creation
    - Optional assignment
    - Activation
    - Onboarding event
    - Post-commit processing
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
                **dict(
                    serializer.validated_data,
                ),
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="employee.onboard",
        )


# =============================================================================
# Offboarding
# =============================================================================


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
                **dict(
                    serializer.validated_data,
                ),
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
