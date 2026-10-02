from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.diagnoses.api.serializers import (
    DiagnosisCreateSerializer,
    DiagnosisSerializer,
    DiagnosisUpdateSerializer,
)
from apps.clinical.diagnoses.permissions.api import DiagnosisAPIPermission
from apps.clinical.diagnoses.selectors import get_diagnoses, get_diagnosis
from apps.clinical.diagnoses.workflows import (
    DiagnosisCreateRequest,
    DiagnosisCreateWorkflow,
    DiagnosisDeleteRequest,
    DiagnosisDeleteWorkflow,
    DiagnosisUpdateRequest,
    DiagnosisUpdateWorkflow,
)
from apps.core.workflows import WorkflowContext


def _organization(request):
    organization = getattr(request.user, "organization", None)
    if organization is None:
        raise PermissionError("Authenticated user has no organization.")
    return organization


def _context(request, name, organization):
    return WorkflowContext(
        tenant_id=organization.tenant_id,
        actor_id=request.user.pk,
        workflow_name=name,
    )


class DiagnosisListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, DiagnosisAPIPermission)

    def get(self, request):
        organization = _organization(request)
        encounter_id = request.query_params.get("encounter")
        queryset = get_diagnoses(
            organization_id=organization.id,
            encounter_id=encounter_id,
        )
        return Response(DiagnosisSerializer(queryset, many=True).data)

    def post(self, request):
        organization = _organization(request)
        serializer = DiagnosisCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = dict(serializer.validated_data)
        encounter = values.pop("encounter")
        diagnosis_code = values.pop("diagnosis_code")
        diagnosis_type = values.pop("diagnosis_type")
        result = DiagnosisCreateWorkflow(
            request=DiagnosisCreateRequest(
                organization_id=organization.id,
                encounter_id=encounter.id,
                diagnosis_code=diagnosis_code,
                diagnosis_type=diagnosis_type,
                data=values,
            )
        ).execute(context=_context(request, "diagnosis.create", organization))
        return Response(
            DiagnosisSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class DiagnosisDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, DiagnosisAPIPermission)

    def get(self, request, diagnosis_id):
        organization = _organization(request)
        record = get_diagnosis(
            organization_id=organization.id, diagnosis_id=diagnosis_id
        )
        return Response(DiagnosisSerializer(record).data)

    def patch(self, request, diagnosis_id):
        organization = _organization(request)
        serializer = DiagnosisUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = DiagnosisUpdateWorkflow(
            request=DiagnosisUpdateRequest(
                organization_id=organization.id,
                diagnosis_id=diagnosis_id,
                data=serializer.validated_data,
            )
        ).execute(context=_context(request, "diagnosis.update", organization))
        return Response(DiagnosisSerializer(result.data).data)

    def delete(self, request, diagnosis_id):
        organization = _organization(request)
        result = DiagnosisDeleteWorkflow(
            request=DiagnosisDeleteRequest(
                organization_id=organization.id,
                diagnosis_id=diagnosis_id,
            )
        ).execute(context=_context(request, "diagnosis.delete", organization))
        return Response(
            DiagnosisSerializer(result.data).data, status=status.HTTP_200_OK
        )
