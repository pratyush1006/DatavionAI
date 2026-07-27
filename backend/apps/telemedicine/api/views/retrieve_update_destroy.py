"""
API views for retrieving, updating, and deleting telemedicine sessions.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.api.responses import success_response
from apps.common.permissions import IsAuthenticatedAndActive
from apps.telemedicine.api.serializers import (
    TelemedicineSessionDetailSerializer,
    TelemedicineSessionUpdateSerializer,
)
from apps.telemedicine.models import TelemedicineSession
from apps.telemedicine.permissions import (
    CanDeleteTelemedicineSession,
    CanUpdateTelemedicineSession,
    CanViewTelemedicineSession,
)
from apps.telemedicine.selectors import SessionSelector
from apps.telemedicine.services import SessionService

SESSION_TAG: Final[tuple[str, ...]] = ("Telemedicine Sessions",)


@extend_schema(tags=SESSION_TAG)
class TelemedicineSessionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a telemedicine session.
    """

    lookup_url_kwarg = "session_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTelemedicineSession,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateTelemedicineSession,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateTelemedicineSession,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteTelemedicineSession,
        ),
    }

    serializer_class = TelemedicineSessionDetailSerializer

    serializer_classes = {
        "GET": TelemedicineSessionDetailSerializer,
        "PUT": TelemedicineSessionUpdateSerializer,
        "PATCH": TelemedicineSessionUpdateSerializer,
    }

    update_service = SessionService.update

    delete_service = SessionService.cancel

    def get_object(
        self,
    ) -> TelemedicineSession:
        """
        Return the requested session.
        """

        return SessionSelector.get(
            session_id=self.kwargs[self.lookup_url_kwarg],
        )


@extend_schema(tags=SESSION_TAG)
class TelemedicineSessionStartAPIView(APIView):
    """
    Start a telemedicine session.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = TelemedicineSessionDetailSerializer

    def post(
        self,
        request: Request,
        session_id: str,
    ) -> Response:
        """
        Start a session.
        """

        session = SessionSelector.get(
            session_id=session_id,
        )

        session = SessionService.start(
            instance=session,
            performed_by=request.user,
        )

        serializer = self.serializer_class(
            session,
        )

        return success_response(
            message="Session started successfully.",
            data=serializer.data,
        )


@extend_schema(tags=SESSION_TAG)
class TelemedicineSessionEndAPIView(APIView):
    """
    End a telemedicine session.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = TelemedicineSessionDetailSerializer

    def post(
        self,
        request: Request,
        session_id: str,
    ) -> Response:
        """
        End a session.
        """

        session = SessionSelector.get(
            session_id=session_id,
        )

        session = SessionService.end(
            instance=session,
            performed_by=request.user,
        )

        serializer = self.serializer_class(
            session,
        )

        return success_response(
            message="Session ended successfully.",
            data=serializer.data,
        )


__all__ = [
    "TelemedicineSessionEndAPIView",
    "TelemedicineSessionRetrieveUpdateDestroyAPIView",
    "TelemedicineSessionStartAPIView",
]
