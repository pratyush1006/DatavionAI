"""REST endpoints for live tracking lifecycle and history."""

from __future__ import annotations

from uuid import UUID

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.geography.api.geography.serializers.tracking import (
    TrackingLocationResponseSerializer,
    TrackingParticipantSerializer,
    TrackingSessionCreateSerializer,
    TrackingSessionSerializer,
)
from apps.platform.geography.models.tracking import TrackingSession
from apps.platform.geography.permissions.tracking import GeographyTrackingPermission
from apps.platform.geography.services.tracking import TrackingService


class TrackingSessionCreateAPIView(APIView):
    permission_classes = (GeographyTrackingPermission,)

    def post(self, request):
        s = TrackingSessionCreateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = TrackingService.start_session(user_id=request.user.pk, **s.validated_data)
        return Response(TrackingSessionSerializer(obj).data, status=201)


class TrackingSessionParticipantAPIView(APIView):
    permission_classes = (GeographyTrackingPermission,)

    def post(self, request, session_id: UUID):
        s = TrackingParticipantSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = TrackingSession.objects.get(pk=session_id)
        if obj.created_by_id != request.user.pk:
            return Response(
                {"detail": "Only the session owner can manage participants."},
                status=403,
            )
        p = TrackingService.add_participant(session_id=session_id, **s.validated_data)
        return Response({"user_id": str(p.user_id), "role": p.role}, status=201)


class TrackingSessionStopAPIView(APIView):
    permission_classes = (GeographyTrackingPermission,)

    def post(self, request, session_id: UUID):
        return Response(
            TrackingSessionSerializer(
                TrackingService.stop_session(
                    session_id=session_id, user_id=request.user.pk
                )
            ).data
        )


class TrackingSessionLocationsAPIView(APIView):
    permission_classes = (GeographyTrackingPermission,)

    def get(self, request, session_id: UUID):
        TrackingService._participant(session_id, request.user.pk)
        rows = TrackingSession.objects.get(pk=session_id).locations.all()[:500]
        return Response(
            TrackingLocationResponseSerializer(
                [TrackingService.serialize_update(x) for x in rows], many=True
            ).data
        )


class TrackingSessionDetailAPIView(APIView):
    permission_classes = (GeographyTrackingPermission,)

    def get(self, request, session_id: UUID):
        TrackingService._participant(session_id, request.user.pk)
        s = TrackingSession.objects.get(pk=session_id)
        data = {
            "id": s.id,
            "tenant_id": s.tenant_id,
            "organization_id": s.organization_id,
            "subject_type": s.subject_type,
            "subject_id": s.subject_id,
            "status": s.status,
            "created_by_id": s.created_by_id,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
            "last_seen_at": s.last_seen_at,
            "last_latitude": (
                float(s.last_latitude) if s.last_latitude is not None else None
            ),
            "last_longitude": (
                float(s.last_longitude) if s.last_longitude is not None else None
            ),
            "last_accuracy_meters": (
                float(s.last_accuracy_meters)
                if s.last_accuracy_meters is not None
                else None
            ),
            "metadata": s.metadata,
        }
        return Response(TrackingSessionSerializer(data).data)


__all__ = (
    "TrackingSessionCreateAPIView",
    "TrackingSessionParticipantAPIView",
    "TrackingSessionStopAPIView",
    "TrackingSessionLocationsAPIView",
    "TrackingSessionDetailAPIView",
)
