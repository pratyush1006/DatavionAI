"""
Patient lifecycle API views.

All Patient lifecycle mutations are workflow driven.

Supported workflows:

    patient.activate
    patient.deactivate
    patient.archive
    patient.restore
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import error_response
from apps.common.exceptions.codes import ErrorCode
from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.patient_management.patients.api.serializers import (
    PatientLifecycleActionSerializer,
)
from apps.patient_management.patients.permissions import (
    CanActivatePatient,
    CanArchivePatient,
    CanDeactivatePatient,
    CanRestorePatient,
)
from apps.patient_management.patients.workflows import (
    PatientActivationRequest,
    PatientActivationWorkflow,
    PatientArchiveRequest,
    PatientArchiveWorkflow,
    PatientDeactivationRequest,
    PatientDeactivationWorkflow,
    PatientRestoreRequest,
    PatientRestoreWorkflow,
)

PATIENT_TAG: Final[tuple[str, ...]] = ("Patients",)


def serialize_workflow_data(
    data: Any,
) -> Any:
    """
    Convert workflow DTO output into API-safe data.
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


def resolve_error_code(
    code: str | None,
) -> ErrorCode:
    """
    Resolve a workflow error code to a platform ErrorCode.
    """

    if not code:
        return ErrorCode.VALIDATION_ERROR

    for error_code in ErrorCode:
        if error_code.value == code:
            return error_code

    member = ErrorCode.__members__.get(
        code.upper(),
    )

    if member is not None:
        return member

    return ErrorCode.VALIDATION_ERROR


def workflow_error_status(
    *,
    result: WorkflowResult[Any],
) -> int:
    """
    Translate workflow semantics into HTTP status.
    """

    from rest_framework import status

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


def workflow_error_details(
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


class PatientWorkflowAPIView(
    BaseGenericAPIView,
):
    """
    Base API view for Patient lifecycle workflows.
    """

    def build_workflow_context(
        self,
        *,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Build workflow context using the established DatavionOS
        tenant-resolution hierarchy.
        """

        tenant = getattr(
            self,
            "current_tenant",
            None,
        )

        if tenant is None:
            organization = getattr(
                self,
                "current_organization",
                None,
            )

            if organization is not None:
                tenant = getattr(
                    organization,
                    "tenant",
                    None,
                )

        if tenant is None:
            user = getattr(
                self,
                "current_user",
                None,
            )

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
                "Tenant context is required for patient lifecycle workflow.",
            )

        actor_id = getattr(
            self.current_user,
            "id",
            None,
        )

        if actor_id is None:
            raise RuntimeError(
                "Authenticated actor is required for patient lifecycle workflow.",
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
        Execute workflow and preserve its success/failure state.
        """

        result = workflow.execute(
            context=self.build_workflow_context(
                workflow_name=workflow_name,
            ),
        )

        if not result.success:
            return error_response(
                code=resolve_error_code(
                    result.code,
                ),
                message=(result.message or "Workflow execution failed."),
                details=workflow_error_details(
                    result,
                ),
                meta={
                    "workflow": workflow_name,
                    "workflow_code": result.code,
                },
                request=self.request,
                status_code=workflow_error_status(
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
                "workflow_code": result.code,
            },
        )


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientActivateAPIView(
    PatientWorkflowAPIView,
):
    """Activate a Patient."""

    permission_classes = (
        IsAuthenticated,
        CanActivatePatient,
    )

    serializer_class = PatientLifecycleActionSerializer

    def post(
        self,
        request,
        patient_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = PatientActivationWorkflow(
            request=PatientActivationRequest(
                patient_id=patient_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="patient.activate",
        )


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientDeactivateAPIView(
    PatientWorkflowAPIView,
):
    """Deactivate a Patient."""

    permission_classes = (
        IsAuthenticated,
        CanDeactivatePatient,
    )

    serializer_class = PatientLifecycleActionSerializer

    def post(
        self,
        request,
        patient_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = PatientDeactivationWorkflow(
            request=PatientDeactivationRequest(
                patient_id=patient_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="patient.deactivate",
        )


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientArchiveAPIView(
    PatientWorkflowAPIView,
):
    """Archive a Patient."""

    permission_classes = (
        IsAuthenticated,
        CanArchivePatient,
    )

    serializer_class = PatientLifecycleActionSerializer

    def post(
        self,
        request,
        patient_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = PatientArchiveWorkflow(
            request=PatientArchiveRequest(
                patient_id=patient_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="patient.archive",
        )


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientRestoreAPIView(
    PatientWorkflowAPIView,
):
    """Restore an archived Patient."""

    permission_classes = (
        IsAuthenticated,
        CanRestorePatient,
    )

    serializer_class = PatientLifecycleActionSerializer

    def post(
        self,
        request,
        patient_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        workflow = PatientRestoreWorkflow(
            request=PatientRestoreRequest(
                patient_id=patient_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="patient.restore",
        )


__all__ = (
    "PatientActivateAPIView",
    "PatientDeactivateAPIView",
    "PatientArchiveAPIView",
    "PatientRestoreAPIView",
)
