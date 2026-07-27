"""
Workflow API views for leave requests.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hr.leave.api.serializers import LeaveRequestDecisionSerializer
from apps.hr.leave.permissions import CanApproveLeaveRequest
from apps.hr.leave.selectors import get_leave_request_by_id
from apps.hr.leave.services import (
    cancel_leave_request,
    decide_leave_request,
)

LEAVE_TAG: Final[tuple[str, ...]] = ("Leave",)


class BaseLeaveRequestWorkflowAPIView(APIView):
    """
    Base workflow API view for leave requests.
    """

    def get_object(self, leave_request_id):
        """
        Return the leave request.
        """

        return get_leave_request_by_id(
            leave_request_id=leave_request_id,
        )


@extend_schema(
    tags=LEAVE_TAG,
    request=LeaveRequestDecisionSerializer,
)
class LeaveRequestApproveAPIView(BaseLeaveRequestWorkflowAPIView):
    """
    Approve a pending leave request.
    """

    permission_classes = (IsAuthenticated, CanApproveLeaveRequest)

    def post(self, request: Request, leave_request_id) -> Response:
        serializer = LeaveRequestDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object(leave_request_id)

        approver = getattr(request.user, "employee_profile", None)

        instance = decide_leave_request(
            instance=instance,
            approver=approver,
            approve=True,
            decision_notes=serializer.validated_data.get(
                "decision_notes",
                "",
            ),
        )

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=LEAVE_TAG,
    request=LeaveRequestDecisionSerializer,
)
class LeaveRequestRejectAPIView(BaseLeaveRequestWorkflowAPIView):
    """
    Reject a pending leave request.
    """

    permission_classes = (IsAuthenticated, CanApproveLeaveRequest)

    def post(self, request: Request, leave_request_id) -> Response:
        serializer = LeaveRequestDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object(leave_request_id)

        approver = getattr(request.user, "employee_profile", None)

        instance = decide_leave_request(
            instance=instance,
            approver=approver,
            approve=False,
            decision_notes=serializer.validated_data.get(
                "decision_notes",
                "",
            ),
        )

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=LEAVE_TAG)
class LeaveRequestCancelAPIView(BaseLeaveRequestWorkflowAPIView):
    """
    Cancel a leave request.
    """

    permission_classes = (IsAuthenticated, CanApproveLeaveRequest)

    def post(self, request: Request, leave_request_id) -> Response:
        instance = self.get_object(leave_request_id)

        instance = cancel_leave_request(instance=instance)

        return Response(
            {"success": True, "status": instance.status},
            status=status.HTTP_200_OK,
        )


__all__ = [
    "LeaveRequestApproveAPIView",
    "LeaveRequestRejectAPIView",
    "LeaveRequestCancelAPIView",
]
