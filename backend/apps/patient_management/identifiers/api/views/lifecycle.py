"""
Workflow-driven API views for Patient Identifier lifecycle operations.

The API layer is intentionally thin:

    HTTP request
        -> serializer validation
        -> workflow request DTO
        -> WorkflowContext
        -> workflow execution
        -> standardized API response

Business rules, authorization decisions, persistence, transactions,
and domain events belong to the workflow/policy/service layers.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.common.api.responses import error_response
from apps.common.exceptions.codes import ErrorCode
from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.patient_management.identifiers.constants import (
    IdentifierSource,
    VerificationStatus,
)
from apps.patient_management.identifiers.permissions import (
    CanActivateIdentifier,
    CanDeactivateIdentifier,
    CanRevokeIdentifier,
    CanSetPrimaryIdentifier,
    CanVerifyIdentifier,
)
from apps.patient_management.identifiers.workflows import (
    IdentifierActivationRequest,
    IdentifierActivationWorkflow,
    IdentifierDeactivationRequest,
    IdentifierDeactivationWorkflow,
    IdentifierPrimaryRequest,
    IdentifierPrimaryWorkflow,
    IdentifierRevocationRequest,
    IdentifierRevocationWorkflow,
    IdentifierVerificationRequest,
    IdentifierVerificationWorkflow,
)

IDENTIFIER_TAG: Final[tuple[str, ...]] = ("Patient Identifiers",)


class IdentifierVerificationActionSerializer(
    serializers.Serializer,
):
    """
    Validate patient identifier verification requests.

    Verification is a terminal decision for the current verification
    operation. A new verification workflow can subsequently be initiated
    if the business process requires re-verification.
    """

    status = serializers.ChoiceField(
        choices=VerificationStatus.choices,
    )

    verification_source = serializers.ChoiceField(
        choices=IdentifierSource.choices,
    )

    reference_number = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate_status(
        self,
        value: str,
    ) -> str:
        """
        Only terminal verification decisions are accepted.
        """

        if value not in {
            VerificationStatus.VERIFIED,
            VerificationStatus.REJECTED,
        }:
            raise serializers.ValidationError(
                "Verification status must be VERIFIED or REJECTED.",
            )

        return value


def serialize_workflow_data(
    data: Any,
) -> Any:
    """
    Convert workflow data into API-safe primitive structures.

    Workflow DTOs may be dataclasses, objects exposing ``to_dict()``,
    or ordinary mappings/objects. Preserve the workflow result contract
    while keeping serialization concerns inside the API layer.
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

    if is_dataclass(data):
        return asdict(data)

    if hasattr(data, "__dict__"):
        return dict(data.__dict__)

    return data


def resolve_error_code(
    code: str | None,
) -> ErrorCode:
    """
    Map workflow error codes to platform API error codes.

    Unknown workflow codes intentionally fall back to the platform
    validation error rather than exposing an invalid API error code.
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


class PatientIdentifierWorkflowAPIView(
    BaseGenericAPIView,
):
    """
    Base API view for patient identifier lifecycle workflows.

    This class owns only API concerns:

    - resolve tenant context
    - resolve authenticated actor
    - construct WorkflowContext
    - execute workflow
    - translate WorkflowResult into API response

    It does not perform identifier persistence or business validation.
    """

    def build_workflow_context(
        self,
        *,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Build a tenant-aware workflow context.

        Tenant resolution follows the established request context first,
        then the current organization, and finally the authenticated
        user's organization role as a defensive fallback.
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
                "Tenant context is required for patient identifier workflow.",
            )

        actor_id = getattr(
            self.current_user,
            "id",
            None,
        )

        if actor_id is None:
            raise RuntimeError(
                "Authenticated actor is required for patient identifier workflow.",
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
        Execute a workflow and translate WorkflowResult into an API response.
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


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierVerifyAPIView(
    PatientIdentifierWorkflowAPIView,
):
    """
    Verify or reject a patient identifier.
    """

    permission_classes = (
        IsAuthenticated,
        CanVerifyIdentifier,
    )

    serializer_class = IdentifierVerificationActionSerializer

    def post(
        self,
        request,
        identifier_id,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        workflow = IdentifierVerificationWorkflow(
            request=IdentifierVerificationRequest(
                identifier_id=identifier_id,
                **dict(serializer.validated_data),
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="identifier.verify",
        )


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierActivateAPIView(
    PatientIdentifierWorkflowAPIView,
):
    """
    Activate a patient identifier.
    """

    permission_classes = (
        IsAuthenticated,
        CanActivateIdentifier,
    )

    def post(
        self,
        request,
        identifier_id,
    ):
        workflow = IdentifierActivationWorkflow(
            request=IdentifierActivationRequest(
                identifier_id=identifier_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="identifier.activate",
        )


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierDeactivateAPIView(
    PatientIdentifierWorkflowAPIView,
):
    """
    Deactivate a patient identifier.
    """

    permission_classes = (
        IsAuthenticated,
        CanDeactivateIdentifier,
    )

    def post(
        self,
        request,
        identifier_id,
    ):
        workflow = IdentifierDeactivationWorkflow(
            request=IdentifierDeactivationRequest(
                identifier_id=identifier_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="identifier.deactivate",
        )


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierRevokeAPIView(
    PatientIdentifierWorkflowAPIView,
):
    """
    Revoke a patient identifier.
    """

    permission_classes = (
        IsAuthenticated,
        CanRevokeIdentifier,
    )

    def post(
        self,
        request,
        identifier_id,
    ):
        workflow = IdentifierRevocationWorkflow(
            request=IdentifierRevocationRequest(
                identifier_id=identifier_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="identifier.revoke",
        )


@extend_schema(
    tags=IDENTIFIER_TAG,
)
class PatientIdentifierSetPrimaryAPIView(
    PatientIdentifierWorkflowAPIView,
):
    """
    Set a patient identifier as primary.
    """

    permission_classes = (
        IsAuthenticated,
        CanSetPrimaryIdentifier,
    )

    def post(
        self,
        request,
        identifier_id,
    ):
        workflow = IdentifierPrimaryWorkflow(
            request=IdentifierPrimaryRequest(
                identifier_id=identifier_id,
            ),
        )

        return self.execute_workflow(
            workflow=workflow,
            workflow_name="identifier.set_primary",
        )


__all__ = (
    "PatientIdentifierActivateAPIView",
    "PatientIdentifierDeactivateAPIView",
    "PatientIdentifierRevokeAPIView",
    "PatientIdentifierSetPrimaryAPIView",
    "PatientIdentifierVerifyAPIView",
)
