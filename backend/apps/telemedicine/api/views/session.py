from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.rbac.resolvers.permission import resolve_permissions
from apps.telemedicine.api.context import require_tenant_organization
from apps.telemedicine.api.serializers import (
    TelemedicineSessionCreateSerializer,
    TelemedicineSessionDetailSerializer,
    TelemedicineSessionUpdateSerializer,
)
from apps.telemedicine.api.workflow import execute_workflow
from apps.telemedicine.selectors import SessionSelector
from apps.telemedicine.services import SessionService
from apps.telemedicine.workflows import *


class TelemedicineSessionListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        _, org = require_tenant_organization(request)
        if "telemedicine.view" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            TelemedicineSessionDetailSerializer(
                SessionSelector.queryset(organization_id=org.id), many=True
            ).data
        )

    def post(self, request):
        tenant, org = require_tenant_organization(request)
        if "telemedicine.create" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        s = TelemedicineSessionCreateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = execute_workflow(
            workflow_class=SessionCreationWorkflow,
            request=request,
            tenant=tenant,
            workflow_name="telemedicine.session.create",
            payload={**s.validated_data, "organization": org},
        )
        if not result.success:
            return Response({"detail": result.message, "code": result.code}, status=400)
        return Response(
            TelemedicineSessionDetailSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class TelemedicineSessionDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, session_id):
        _, org = require_tenant_organization(request)
        if "telemedicine.view" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        s = SessionSelector.get(session_id=session_id, organization_id=org.id)
        return Response(TelemedicineSessionDetailSerializer(s).data)

    def patch(self, request, session_id):
        _, org = require_tenant_organization(request)
        if "telemedicine.update" not in resolve_permissions(
            user=request.user, organization=org
        ):
            return Response({"detail": "Permission denied."}, status=403)
        s = SessionSelector.get(session_id=session_id, organization_id=org.id)
        ser = TelemedicineSessionUpdateSerializer(s, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        return Response(
            TelemedicineSessionDetailSerializer(
                SessionService.update(session=s, validated_data=ser.validated_data)
            ).data
        )


class TelemedicineSessionActionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    WF = {
        "schedule": (SessionSchedulingWorkflow, "telemedicine.session.schedule"),
        "confirm": (SessionConfirmationWorkflow, "telemedicine.session.confirm"),
        "prepare": (SessionPreparationWorkflow, "telemedicine.session.prepare"),
        "start": (SessionStartWorkflow, "telemedicine.session.start"),
        "complete": (SessionCompletionWorkflow, "telemedicine.session.complete"),
        "cancel": (SessionCancellationWorkflow, "telemedicine.session.cancel"),
        "no-show": (SessionNoShowWorkflow, "telemedicine.session.no_show"),
        "fail": (SessionFailureWorkflow, "telemedicine.session.fail"),
    }

    def post(self, request, session_id, action):
        tenant, org = require_tenant_organization(request)
        s = SessionSelector.get(session_id=session_id, organization_id=org.id)
        item = self.WF.get(action)
        if not item:
            return Response({"detail": "Unknown action."}, status=400)
        required = {
            "start": "telemedicine.start",
            "complete": "telemedicine.complete",
            "cancel": "telemedicine.cancel",
            "prepare": "telemedicine.prepare",
        }.get(action, "telemedicine.update")
        if required not in resolve_permissions(user=request.user, organization=org):
            return Response({"detail": "Permission denied."}, status=403)
        cls, name = item
        result = execute_workflow(
            workflow_class=cls,
            request=request,
            tenant=tenant,
            workflow_name=name,
            payload={
                "session_id": s.session_id,
                "organization_id": org.id,
                "cancellation_reason": request.data.get("cancellation_reason", ""),
                "failure_reason": request.data.get("failure_reason", ""),
            },
        )
        if not result.success:
            return Response({"detail": result.message, "code": result.code}, status=400)
        return Response(TelemedicineSessionDetailSerializer(result.data).data)
