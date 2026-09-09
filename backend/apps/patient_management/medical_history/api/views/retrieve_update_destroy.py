"""Retrieve Update Destroy."""

from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.workflows import WorkflowContext
from apps.patient_management.medical_history.api.serializers import (
    MedicalHistoryDetailSerializer,
    MedicalHistoryUpdateSerializer,
)
from apps.patient_management.medical_history.models import PatientMedicalHistory
from apps.patient_management.medical_history.permissions import (
    CanDeleteMedicalHistory,
    CanUpdateMedicalHistory,
    CanViewMedicalHistory,
)
from apps.patient_management.medical_history.selectors import get_medical_history
from apps.patient_management.medical_history.workflows import (
    MedicalHistoryDeletionRequest,
    MedicalHistoryDeletionWorkflow,
    MedicalHistoryUpdateRequest,
    MedicalHistoryUpdateWorkflow,
)


def _raise_workflow_error(result):
    """raise workflow error."""
    if result.success:
        return
    code = str(getattr(result, "code", "workflow_error") or "workflow_error")
    message = getattr(result, "message", None) or "The requested operation failed."
    if "not_found" in code:
        raise NotFound(message)
    if any(token in code for token in ("permission", "denied", "forbidden")):
        raise PermissionDenied(message)
    error = APIException(message)
    error.default_code = code
    raise error


class MedicalHistoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """MedicalHistoryRetrieveUpdateDestroyAPIView implementation."""

    def get_permissions(self):
        """Get permissions."""
        if self.request.method in ("PUT", "PATCH"):
            return [IsAuthenticated(), CanUpdateMedicalHistory()]
        if self.request.method == "DELETE":
            return [IsAuthenticated(), CanDeleteMedicalHistory()]
        return [IsAuthenticated(), CanViewMedicalHistory()]

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

    def get_object(self):
        """Get object."""
        try:
            return get_medical_history(
                tenant_id=self.get_tenant().id, history_id=self.kwargs["pk"]
            )
        except PatientMedicalHistory.DoesNotExist as exc:
            raise NotFound("Medical history was not found.") from exc

    def get_serializer_class(self):
        """Get serializer class."""
        return (
            MedicalHistoryUpdateSerializer
            if self.request.method in ("PUT", "PATCH")
            else MedicalHistoryDetailSerializer
        )

    def update(self, request, *args, **kwargs):
        """Update."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=kwargs.get("partial", False)
        )
        serializer.is_valid(raise_exception=True)
        try:
            result = MedicalHistoryUpdateWorkflow(
                request=MedicalHistoryUpdateRequest(
                    history_id=instance.pk, data=dict(serializer.validated_data)
                )
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
        _raise_workflow_error(result)
        instance = get_medical_history(
            tenant_id=self.get_tenant().id, history_id=instance.pk
        )
        return Response(
            MedicalHistoryDetailSerializer(instance, context={"request": request}).data
        )

    def destroy(self, request, *args, **kwargs):
        """Destroy."""
        instance = self.get_object()
        try:
            result = MedicalHistoryDeletionWorkflow(
                request=MedicalHistoryDeletionRequest(history_id=instance.pk)
            ).execute(
                context=WorkflowContext(
                    actor_id=request.user.id, tenant_id=self.get_tenant().id
                )
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc)) from exc
        except ValueError as exc:
            raise NotFound(str(exc)) from exc
        _raise_workflow_error(result)
        return Response(status=204)


__all__ = ("MedicalHistoryRetrieveUpdateDestroyAPIView",)
