from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.encounters.api.serializers import (
    EncounterCreateSerializer,
    EncounterSerializer,
    EncounterUpdateSerializer,
)
from apps.clinical.encounters.permissions.api import EncounterAPIPermission
from apps.clinical.encounters.selectors import get_encounter, get_encounters
from apps.clinical.encounters.workflows import (
    EncounterCancelWorkflow,
    EncounterCompleteWorkflow,
    EncounterCreateRequest,
    EncounterCreateWorkflow,
    EncounterDeleteWorkflow,
    EncounterLifecycleRequest,
    EncounterStartWorkflow,
    EncounterUpdateRequest,
    EncounterUpdateWorkflow,
)
from apps.core.workflows import WorkflowContext


def _organization(request):
    organization = getattr(request.user, "organization", None)
    if organization is None:
        raise PermissionError("Authenticated user has no organization context.")
    return organization


def _context(request, name, organization):
    return WorkflowContext(
        tenant_id=organization.tenant_id,
        actor_id=request.user.pk,
        workflow_name=name,
    )


class EncounterListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, EncounterAPIPermission)

    def get(self, request):
        organization = _organization(request)
        queryset = get_encounters(organization_id=organization.id)
        return Response(EncounterSerializer(queryset, many=True).data)

    def post(self, request):
        organization = _organization(request)
        serializer = EncounterCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = dict(serializer.validated_data)
        appointment = values.pop("appointment")
        patient = values.pop("patient")
        provider = values.pop("provider")
        number = values.pop("encounter_number")
        result = EncounterCreateWorkflow(
            request=EncounterCreateRequest(
                organization_id=organization.id,
                appointment_id=appointment.id,
                patient_id=patient.id,
                provider_id=provider.id,
                encounter_number=number,
                data=values,
            )
        ).execute(context=_context(request, "encounter.create", organization))
        return Response(
            EncounterSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class EncounterDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, EncounterAPIPermission)

    def get(self, request, encounter_id):
        organization = _organization(request)
        record = get_encounter(
            organization_id=organization.id, encounter_id=encounter_id
        )
        return Response(EncounterSerializer(record).data)

    def patch(self, request, encounter_id):
        organization = _organization(request)
        serializer = EncounterUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = EncounterUpdateWorkflow(
            request=EncounterUpdateRequest(
                organization_id=organization.id,
                encounter_id=encounter_id,
                data=serializer.validated_data,
            )
        ).execute(context=_context(request, "encounter.update", organization))
        return Response(EncounterSerializer(result.data).data)

    def delete(self, request, encounter_id):
        organization = _organization(request)
        result = EncounterDeleteWorkflow(
            request=EncounterLifecycleRequest(
                organization_id=organization.id,
                encounter_id=encounter_id,
            )
        ).execute(context=_context(request, "encounter.delete", organization))
        return Response(EncounterSerializer(result.data).data)


class EncounterLifecycleAPIView(APIView):
    permission_classes = (IsAuthenticated, EncounterAPIPermission)

    ACTIONS = {
        "start": (EncounterStartWorkflow, "encounter.start"),
        "complete": (EncounterCompleteWorkflow, "encounter.complete"),
        "cancel": (EncounterCancelWorkflow, "encounter.cancel"),
    }

    def post(self, request, encounter_id, action):
        workflow_class, workflow_name = self.ACTIONS[action]
        organization = _organization(request)
        result = workflow_class(
            request=EncounterLifecycleRequest(
                organization_id=organization.id,
                encounter_id=encounter_id,
            )
        ).execute(context=_context(request, workflow_name, organization))
        return Response(EncounterSerializer(result.data).data)
