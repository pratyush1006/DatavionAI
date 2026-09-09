"""Patient Preferences API views."""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.mixins.workflows import WorkflowMixin
from apps.patient_management.preferences.api.serializers import (
    PatientCommunicationPreferenceRequestSerializer,
    PatientPreferenceCreateSerializer,
    PatientPreferenceDetailSerializer,
    PatientPreferenceListSerializer,
    PatientPreferenceUpdateSerializer,
)
from apps.patient_management.preferences.permissions import (
    CanCreatePatientPreference,
    CanDeletePatientPreference,
    CanListPatientPreferences,
    CanManageCommunicationPreference,
    CanRestorePatientPreference,
    CanUpdatePatientPreference,
    CanViewPatientPreference,
)
from apps.patient_management.preferences.selectors import PatientPreferenceSelector
from apps.patient_management.preferences.workflows import (
    PatientCommunicationPreferenceRequest,
    PatientCommunicationPreferenceWorkflow,
    PatientPreferenceCreationRequest,
    PatientPreferenceCreationWorkflow,
    PatientPreferenceDeletionRequest,
    PatientPreferenceDeletionWorkflow,
    PatientPreferenceRestoreRequest,
    PatientPreferenceRestoreWorkflow,
    PatientPreferenceUpdateRequest,
    PatientPreferenceUpdateWorkflow,
)


def _organization(request):
    """Resolve the request organization using the established tenant pattern."""

    organization = getattr(request, "organization", None)
    if organization is not None:
        return organization

    role = (
        request.user.organization_roles.select_related("organization__tenant")
        .filter(organization__tenant_id=getattr(request, "tenant_id", None))
        .first()
    )
    if role is None:
        role = request.user.organization_roles.select_related(
            "organization__tenant"
        ).first()

    if role is None:
        raise ValueError("No organization is available for the current user.")

    return role.organization


class PatientPreferenceListCreateAPIView(WorkflowMixin, APIView):
    """List and create Patient Preferences."""

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """Return operation-specific permissions for the collection endpoint."""

        permissions = [IsAuthenticated()]

        if self.request.method == "GET":
            permissions.append(CanListPatientPreferences())
        elif self.request.method == "POST":
            permissions.append(CanCreatePatientPreference())

        return permissions

    def get(self, request):
        """Return organization-scoped patient preferences."""

        organization = _organization(request)
        queryset = PatientPreferenceSelector.list(
            organization_id=organization.id,
            tenant_id=organization.tenant_id,
        )
        return Response(
            PatientPreferenceListSerializer(
                queryset,
                many=True,
            ).data,
        )

    def post(self, request):
        """Create or initialize one patient's preferences."""

        serializer = PatientPreferenceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = _organization(request)

        result = PatientPreferenceCreationWorkflow(
            request=PatientPreferenceCreationRequest(
                organization_id=organization.id,
                patient_id=serializer.validated_data.pop("patient_id"),
                data=serializer.validated_data,
            ),
        ).run(
            context=self.workflow_context(request),
        )

        return Response(
            {"preference_id": str(result.data.preference_id)},
            status=status.HTTP_201_CREATED,
        )


class PatientPreferenceDetailAPIView(WorkflowMixin, APIView):
    """Retrieve and update one Patient Preference."""

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """Return operation-specific permissions for the detail endpoint."""

        permissions = [IsAuthenticated()]

        if self.request.method == "GET":
            permissions.append(CanViewPatientPreference())
        elif self.request.method == "PATCH":
            permissions.append(CanUpdatePatientPreference())

        return permissions

    def get(self, request, preference_id):
        """Return one patient preference."""

        organization = _organization(request)
        preference = PatientPreferenceSelector.get(
            preference_id=preference_id,
            organization_id=organization.id,
            tenant_id=organization.tenant_id,
        )
        return Response(
            PatientPreferenceDetailSerializer(preference).data,
        )

    def patch(self, request, preference_id):
        """Update one patient preference."""

        serializer = PatientPreferenceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = _organization(request)

        result = PatientPreferenceUpdateWorkflow(
            request=PatientPreferenceUpdateRequest(
                organization_id=organization.id,
                preference_id=preference_id,
                data=serializer.validated_data,
            ),
        ).run(
            context=self.workflow_context(request),
        )

        return Response(
            {"preference_id": str(result.data.preference_id)},
        )


class PatientPreferenceDeleteAPIView(WorkflowMixin, APIView):
    """Soft-delete one Patient Preference."""

    permission_classes = (
        IsAuthenticated,
        CanDeletePatientPreference,
    )

    def delete(self, request, preference_id):
        """Soft-delete the selected preference."""

        organization = _organization(request)
        result = PatientPreferenceDeletionWorkflow(
            request=PatientPreferenceDeletionRequest(
                organization_id=organization.id,
                preference_id=preference_id,
            ),
        ).run(
            context=self.workflow_context(request),
        )
        return Response(
            {"preference_id": str(result.data)},
            status=status.HTTP_204_NO_CONTENT,
        )


class PatientPreferenceRestoreAPIView(WorkflowMixin, APIView):
    """Restore one deleted Patient Preference."""

    permission_classes = (
        IsAuthenticated,
        CanRestorePatientPreference,
    )

    def post(self, request, preference_id):
        """Restore the selected preference."""

        organization = _organization(request)
        result = PatientPreferenceRestoreWorkflow(
            request=PatientPreferenceRestoreRequest(
                organization_id=organization.id,
                preference_id=preference_id,
            ),
        ).run(
            context=self.workflow_context(request),
        )
        return Response(
            {"preference_id": str(result.data)},
        )


class PatientCommunicationPreferenceAPIView(WorkflowMixin, APIView):
    """Create or update a communication channel preference."""

    permission_classes = (
        IsAuthenticated,
        CanManageCommunicationPreference,
    )

    def put(self, request, preference_id):
        """Set one communication channel preference."""

        serializer = PatientCommunicationPreferenceRequestSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        organization = _organization(request)
        channel = serializer.validated_data.pop("channel")

        result = PatientCommunicationPreferenceWorkflow(
            request=PatientCommunicationPreferenceRequest(
                organization_id=organization.id,
                preference_id=preference_id,
                channel=channel,
                data=serializer.validated_data,
            ),
        ).run(
            context=self.workflow_context(request),
        )
        return Response(
            {"communication_preference_id": str(result.data)},
        )


__all__ = (
    "PatientCommunicationPreferenceAPIView",
    "PatientPreferenceDeleteAPIView",
    "PatientPreferenceDetailAPIView",
    "PatientPreferenceListCreateAPIView",
    "PatientPreferenceRestoreAPIView",
)
