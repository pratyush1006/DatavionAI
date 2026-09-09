"""List Create."""

from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.workflows import WorkflowContext
from apps.patient_management.medical_history.api.filters import MedicalHistoryFilter
from apps.patient_management.medical_history.api.serializers import (
    MedicalHistoryCreateSerializer,
    MedicalHistoryDetailSerializer,
    MedicalHistoryListSerializer,
)
from apps.patient_management.medical_history.permissions import (
    CanCreateMedicalHistory,
    CanListMedicalHistory,
)
from apps.patient_management.medical_history.selectors import (
    get_medical_history,
    list_medical_history,
)
from apps.patient_management.medical_history.workflows import (
    MedicalHistoryCreationRequest,
    MedicalHistoryCreationWorkflow,
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


class MedicalHistoryListCreateAPIView(generics.ListCreateAPIView):
    """MedicalHistoryListCreateAPIView implementation."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = MedicalHistoryFilter

    def get_permissions(self):
        """Get permissions."""
        return (
            [IsAuthenticated(), CanCreateMedicalHistory()]
            if self.request.method == "POST"
            else [IsAuthenticated(), CanListMedicalHistory()]
        )

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

    def get_queryset(self):
        """Get queryset."""
        return list_medical_history(
            tenant_id=self.get_tenant().id, include_inactive=True
        )

    def get_serializer_class(self):
        """Get serializer class."""
        return (
            MedicalHistoryCreateSerializer
            if self.request.method == "POST"
            else MedicalHistoryListSerializer
        )

    def create(self, request, *args, **kwargs):
        """Create."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        organization_id, patient_id = (
            data.pop("organization_id"),
            data.pop("patient_id"),
        )
        try:
            result = MedicalHistoryCreationWorkflow(
                request=MedicalHistoryCreationRequest(
                    organization_id=organization_id, patient_id=patient_id, data=data
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
            tenant_id=self.get_tenant().id, history_id=result.data.history_id
        )
        return Response(
            MedicalHistoryDetailSerializer(instance, context={"request": request}).data,
            status=201,
        )


__all__ = ("MedicalHistoryListCreateAPIView",)
