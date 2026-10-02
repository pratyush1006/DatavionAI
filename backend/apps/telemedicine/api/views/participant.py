from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.rbac.resolvers.permission import resolve_permissions
from apps.telemedicine.api.context import require_tenant_organization
from apps.telemedicine.api.serializers import (
    ParticipantMediaStateSerializer,
    ParticipantSerializer,
)
from apps.telemedicine.api.workflow import execute_workflow
from apps.telemedicine.models import Participant
from apps.telemedicine.workflows import (
    ParticipantAdmissionWorkflow,
    ParticipantInvitationWorkflow,
    ParticipantJoinWorkflow,
    ParticipantLeaveWorkflow,
    ParticipantMediaStateWorkflow,
)


class ParticipantListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, session_id):
        _, org = require_tenant_organization(request)
        if "telemedicine.participant.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        qs = Participant.objects.filter(
            session_id=session_id, session__organization_id=org.id
        ).select_related("user")
        return Response(ParticipantSerializer(qs, many=True).data)

    def post(self, request, session_id):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.participant.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        ser = ParticipantSerializer(data={**request.data, "session": session_id})
        ser.is_valid(raise_exception=True)
        r = execute_workflow(
            workflow_class=ParticipantInvitationWorkflow,
            request=request,
            tenant=tenant,
            workflow_name="telemedicine.participant.invite",
            payload={
                "session_id": session_id,
                "organization_id": org.id,
                "user_id": ser.validated_data["user"].pk,
                "participant_type": ser.validated_data["participant_type"],
            },
        )
        if not r.success:
            return Response({"detail": r.message}, status=400)
        return Response(
            ParticipantSerializer(r.data).data, status=status.HTTP_201_CREATED
        )


class ParticipantActionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    WF = {
        "admit": (ParticipantAdmissionWorkflow, "telemedicine.participant.admit"),
        "join": (ParticipantJoinWorkflow, "telemedicine.participant.join"),
        "leave": (ParticipantLeaveWorkflow, "telemedicine.participant.leave"),
    }

    def post(self, request, participant_id, action):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.participant.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        if action not in self.WF:
            return Response({"detail": "Unknown action."}, status=400)
        cls, name = self.WF[action]
        r = execute_workflow(
            workflow_class=cls,
            request=request,
            tenant=tenant,
            workflow_name=name,
            payload={"participant_id": participant_id, "organization_id": org.id},
        )
        if not r.success:
            return Response({"detail": r.message}, status=400)
        return Response(ParticipantSerializer(r.data).data)


class ParticipantMediaStateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, participant_id):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.participant.manage" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        ser = ParticipantMediaStateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        r = execute_workflow(
            workflow_class=ParticipantMediaStateWorkflow,
            request=request,
            tenant=tenant,
            workflow_name="telemedicine.participant.media_state",
            payload={
                "participant_id": participant_id,
                "organization_id": org.id,
                "data": ser.validated_data,
            },
        )
        if not r.success:
            return Response({"detail": r.message}, status=400)
        return Response(ParticipantSerializer(r.data).data)
