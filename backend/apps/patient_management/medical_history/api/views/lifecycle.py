"""Lifecycle."""

from __future__ import annotations

from dataclasses import asdict

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.medical_history.permissions import (
    CanActivateMedicalHistory,
    CanDeactivateMedicalHistory,
    CanRestoreMedicalHistory,
    CanVerifyMedicalHistory,
)
from apps.patient_management.medical_history.workflows import (
    MedicalHistoryActivationWorkflow,
    MedicalHistoryDeactivationWorkflow,
    MedicalHistoryLifecycleRequest,
    MedicalHistoryRestoreWorkflow,
    MedicalHistoryVerificationRequest,
    MedicalHistoryVerificationWorkflow,
)


class MedicalHistoryLifecycleBaseAPIView(APIView):
    """MedicalHistoryLifecycleBaseAPIView implementation."""

    workflow = None
    permission_class = None

    def get_permissions(self):
        """Get permissions."""
        return [IsAuthenticated(), self.permission_class()]

    def get_tenant(self):
        """Get tenant."""
        tenant = (
            getattr(self.request, "tenant", None)
            or getattr(self, "current_tenant", None)
            or getattr(self.request.user, "tenant", None)
        )
        if tenant is None:
            role = self.request.user.organization_roles.select_related(
                "organization__tenant"
            ).first()
            tenant = role.organization.tenant if role else None
        if tenant is None:
            raise DRFValidationError({"detail": "Tenant context is required."})
        return tenant

    def execute(self, request, pk):
        """Execute."""
        try:
            return self.workflow(
                request=MedicalHistoryLifecycleRequest(history_id=pk)
            ).execute(
                context=WorkflowContext(
                    actor_id=request.user.id, tenant_id=self.get_tenant().id
                )
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc)) from exc
        except ValueError as exc:
            raise NotFound(str(exc)) from exc
        except DjangoValidationError as exc:
            raise DRFValidationError(
                exc.message_dict if hasattr(exc, "message_dict") else exc.messages
            ) from exc

    def post(self, request, pk):
        """Post."""
        result = self.execute(request, pk)
        if not result.success:
            error = APIException(result.message or "Lifecycle operation failed.")
            error.default_code = str(getattr(result, "code", "workflow_error"))
            raise error
        return Response(
            {
                "message": result.message,
                "code": result.code,
                "data": asdict(result.data),
            }
        )


class MedicalHistoryActivateAPIView(MedicalHistoryLifecycleBaseAPIView):
    """MedicalHistoryActivateAPIView implementation."""

    workflow = MedicalHistoryActivationWorkflow
    permission_class = CanActivateMedicalHistory


class MedicalHistoryDeactivateAPIView(MedicalHistoryLifecycleBaseAPIView):
    """MedicalHistoryDeactivateAPIView implementation."""

    workflow = MedicalHistoryDeactivationWorkflow
    permission_class = CanDeactivateMedicalHistory


class MedicalHistoryRestoreAPIView(MedicalHistoryLifecycleBaseAPIView):
    """MedicalHistoryRestoreAPIView implementation."""

    workflow = MedicalHistoryRestoreWorkflow
    permission_class = CanRestoreMedicalHistory


class MedicalHistoryVerifyAPIView(MedicalHistoryLifecycleBaseAPIView):
    """MedicalHistoryVerifyAPIView implementation."""

    workflow = MedicalHistoryVerificationWorkflow
    permission_class = CanVerifyMedicalHistory

    def post(self, request, pk):
        """Post."""
        try:
            result = self.workflow(
                request=MedicalHistoryVerificationRequest(history_id=pk)
            ).execute(
                context=WorkflowContext(
                    actor_id=request.user.id, tenant_id=self.get_tenant().id
                )
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc)) from exc
        except ValueError as exc:
            raise NotFound(str(exc)) from exc
        except DjangoValidationError as exc:
            raise DRFValidationError(
                exc.message_dict if hasattr(exc, "message_dict") else exc.messages
            ) from exc
        if not result.success:
            error = APIException(result.message or "Verification failed.")
            error.default_code = str(getattr(result, "code", "workflow_error"))
            raise error
        return Response(
            {
                "message": result.message,
                "code": result.code,
                "data": asdict(result.data),
            }
        )


__all__ = (
    "MedicalHistoryLifecycleBaseAPIView",
    "MedicalHistoryActivateAPIView",
    "MedicalHistoryDeactivateAPIView",
    "MedicalHistoryRestoreAPIView",
    "MedicalHistoryVerifyAPIView",
)
