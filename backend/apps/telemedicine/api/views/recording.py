from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.rbac.resolvers.permission import resolve_permissions
from apps.telemedicine.api.context import require_tenant_organization
from apps.telemedicine.api.serializers import RecordingSerializer
from apps.telemedicine.api.workflow import execute_workflow
from apps.telemedicine.models import Recording
from apps.telemedicine.workflows import (
    RecordingFinalizeWorkflow,
    RecordingStartWorkflow,
)


class RecordingListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, session_id):
        _, org = require_tenant_organization(request)
        if "telemedicine.recording.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            RecordingSerializer(
                Recording.objects.filter(
                    session_id=session_id, session__organization_id=org.id
                ),
                many=True,
            ).data
        )


class RecordingStartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, session_id):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.recording.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        r = execute_workflow(
            workflow_class=RecordingStartWorkflow,
            request=request,
            tenant=tenant,
            workflow_name="telemedicine.recording.start",
            payload={"session_id": session_id, "organization_id": org.id},
        )
        if not r.success:
            return Response({"detail": r.message}, status=400)
        return Response(
            RecordingSerializer(r.data).data, status=status.HTTP_201_CREATED
        )


class RecordingFinalizeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recording_id):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.recording.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        r = execute_workflow(
            workflow_class=RecordingFinalizeWorkflow,
            request=request,
            tenant=tenant,
            workflow_name="telemedicine.recording.finalize",
            payload={
                "recording_id": recording_id,
                "organization_id": org.id,
                "recording_url": request.data.get("recording_url", ""),
                "duration_seconds": request.data.get("duration_seconds"),
                "file_size_bytes": request.data.get("file_size_bytes"),
                "transcript_url": request.data.get("transcript_url", ""),
            },
        )
        if not r.success:
            return Response({"detail": r.message}, status=400)
        return Response(RecordingSerializer(r.data).data)
