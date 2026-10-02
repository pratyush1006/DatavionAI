"""
Workflow-driven API views for Patient Registration lifecycle operations.

Architecture
------------

HTTP request
    -> serializer validation
    -> workflow request
    -> WorkflowContext
    -> workflow execution
    -> standardized API response

Business rules, authorization, persistence, transactions, and domain
events belong to the workflow/policy/service layers.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Final

from apps.common.api.base_generics import BaseGenericAPIView
from apps.common.api.responses import error_response
from apps.common.exceptions.codes import ErrorCode
from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.patient_management.registration.permissions import (
    CanCancelRegistration,
    CanCheckInRegistration,
    CanCompleteRegistration,
    CanNoShowRegistration,
    CanRejectRegistration,
    CanVerifyRegistration,
)
from apps.patient_management.registration.workflows import (
    RegistrationCancellationRequest,
    RegistrationCancellationWorkflow,
    RegistrationCheckInRequest,
    RegistrationCheckInWorkflow,
    RegistrationCompletionRequest,
    RegistrationCompletionWorkflow,
    RegistrationNoShowRequest,
    RegistrationNoShowWorkflow,
    RegistrationRejectionRequest,
    RegistrationRejectionWorkflow,
    RegistrationVerificationRequest,
    RegistrationVerificationWorkflow,
)
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

REGISTRATION_TAG: Final[tuple[str, ...]] = ("Patient Registrations",)


class RegistrationCancellationSerializer(
    serializers.Serializer,
):
    """
    Validate registration cancellation input.
    """

    reason = serializers.CharField(
        max_length=255,
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
    )

    def validate_reason(
        self,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Cancellation reason is required.")

        return value

    def validate_notes(
        self,
        value: str,
    ) -> str:
        return value.strip()


def serialize_workflow_data(
    data: Any,
) -> Any:
    """
    Convert workflow result data into API-safe primitives.
    """

    if data is None:
        return None

    to_dict = getattr(
        data,
        "to_dict",
        None,
    )

    if callable(to_dict):
        return to_dict()

    if is_dataclass(data) and not isinstance(data, type):
        return asdict(data)

    if hasattr(data, "__dict__"):
        return dict(data.__dict__)

    return data


def resolve_error_code(
    code: str | None,
) -> ErrorCode:
    """
    Map workflow error codes to platform API error codes.
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


class PatientRegistrationWorkflowAPIView(
    BaseGenericAPIView,
):
    """
    Base API view for registration lifecycle workflows.

    This class contains no registration business logic.
    """

    def _resolve_organization(self):
        """
        Resolve the organization from the authenticated request context.

        Organization is derived from trusted request context and is never
        accepted as client-controlled workflow input.
        """

        organization = self.current_organization

        if organization is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

        if organization is None:
            user = self.current_user

            organization_roles = getattr(
                user,
                "organization_roles",
                None,
            )

            if organization_roles is not None:
                organization_role = organization_roles.select_related(
                    "organization__tenant"
                ).first()

                if organization_role is not None:
                    organization = organization_role.organization

        if organization is None:
            raise NotFound("Organization context is required.")

        return organization

    def build_workflow_context(
        self,
        *,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Build a tenant-aware workflow context.
        """

        tenant = self.current_tenant

        if tenant is None:
            organization = self._resolve_organization()

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
                    "organization__tenant"
                ).first()

                if organization_role is not None:
                    tenant = organization_role.organization.tenant

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required for patient registration workflow."
            )

        actor_id = getattr(
            self.current_user,
            "id",
            None,
        )

        if actor_id is None:
            raise RuntimeError(
                "Authenticated actor is required for patient registration workflow."
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
        Execute a workflow and translate its result into an API response.
        """

        context = self.build_workflow_context(
            workflow_name=workflow_name,
        )

        result: WorkflowResult[Any] = workflow.execute(
            context=context,
        )

        if not result.success:
            details = None

            if result.error is not None:
                to_dict = getattr(
                    result.error,
                    "to_dict",
                    None,
                )

                if callable(to_dict):
                    details = to_dict()
                else:
                    details = getattr(
                        result.error,
                        "details",
                        None,
                    )

            return error_response(
                code=resolve_error_code(
                    result.code,
                ),
                message=(result.message or "Workflow execution failed."),
                details=details,
                meta={
                    "workflow": workflow_name,
                    "workflow_code": result.code,
                },
                request=self.request,
                status_code=400,
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


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationVerifyAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Verify a patient registration.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanVerifyRegistration,
        ),
    }

    def post(
        self,
        request,
        registration_id,
    ):
        organization = self._resolve_organization()

        workflow = RegistrationVerificationWorkflow(
            request=RegistrationVerificationRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.verify",
        )


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationCheckInAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Check in a patient registration.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanCheckInRegistration,
        ),
    }

    def post(
        self,
        request,
        registration_id,
    ):
        organization = self._resolve_organization()

        workflow = RegistrationCheckInWorkflow(
            request=RegistrationCheckInRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.check_in",
        )


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationCompleteAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Complete a patient registration.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanCompleteRegistration,
        ),
    }

    def post(
        self,
        request,
        registration_id,
    ):
        organization = self._resolve_organization()

        workflow = RegistrationCompletionWorkflow(
            request=RegistrationCompletionRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.complete",
        )


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationCancelAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Cancel a patient registration.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanCancelRegistration,
        ),
    }

    serializer_class = RegistrationCancellationSerializer

    def post(
        self,
        request,
        registration_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        organization = self._resolve_organization()

        workflow = RegistrationCancellationWorkflow(
            request=RegistrationCancellationRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
                reason=serializer.validated_data["reason"],
                notes=serializer.validated_data.get(
                    "notes",
                    "",
                ),
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.cancel",
        )


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationRejectAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Reject a patient registration.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanRejectRegistration,
        ),
    }

    def post(
        self,
        request,
        registration_id,
    ):
        organization = self._resolve_organization()

        workflow = RegistrationRejectionWorkflow(
            request=RegistrationRejectionRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.reject",
        )


@extend_schema(tags=REGISTRATION_TAG)
class PatientRegistrationNoShowAPIView(
    PatientRegistrationWorkflowAPIView,
):
    """
    Mark a patient registration as a no-show.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanNoShowRegistration,
        ),
    }

    def post(
        self,
        request,
        registration_id,
    ):
        organization = self._resolve_organization()

        workflow = RegistrationNoShowWorkflow(
            request=RegistrationNoShowRequest(
                organization_id=organization.pk,
                registration_id=registration_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="registration.no_show",
        )


__all__ = (
    "PatientRegistrationCancelAPIView",
    "PatientRegistrationCheckInAPIView",
    "PatientRegistrationCompleteAPIView",
    "PatientRegistrationNoShowAPIView",
    "PatientRegistrationRejectAPIView",
    "PatientRegistrationVerifyAPIView",
)
