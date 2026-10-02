"""
REST API for the clinical transcription bounded context.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta

from apps.common.api.responses import success_response
from apps.transcription.api.context import require_tenant_organization
from apps.transcription.api.serializers.jobs import (
    TranscriptionJobCreateSerializer,
    TranscriptionJobSerializer,
)
from apps.transcription.api.serializers.notes import (
    ClinicalNoteGenerateSerializer,
    ClinicalNoteReviewSerializer,
    GeneratedNoteSerializer,
    GeneratedNoteUpdateSerializer,
)
from apps.transcription.api.workflow import execute_workflow
from apps.transcription.models import LiveTranscriptionSession
from apps.transcription.rbac import has_permission
from apps.transcription.selectors import GeneratedNoteSelector, TranscriptionJobSelector
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows import (
    ClinicalNoteGenerateWorkflow,
    ClinicalNoteReviewWorkflow,
    ClinicalNoteSignWorkflow,
    TranscriptionJobCancelWorkflow,
    TranscriptionJobCreateWorkflow,
    TranscriptionJobQueueWorkflow,
    TranscriptionJobRunWorkflow,
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LiveTranscriptionTicketAPIView(APIView):
    """Issue a short-lived one-use WebSocket ticket to an authorized session owner."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, session_id):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.run",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        session = get_object_or_404(
            LiveTranscriptionSession,
            session_id=session_id,
            organization=organization,
            created_by=request.user,
        )
        ticket = secrets.token_urlsafe(32)
        session.websocket_ticket_hash = hashlib.sha256(
            ticket.encode("utf-8"),
        ).hexdigest()
        session.websocket_ticket_expires_at = timezone.now() + timedelta(seconds=60)
        session.save(
            update_fields=(
                "websocket_ticket_hash",
                "websocket_ticket_expires_at",
                "updated_at",
            )
        )
        return success_response(data={"ticket": ticket}, request=request)


class LiveSessionNoteGenerateAPIView(APIView):
    """Generate a clinician-reviewable note from a completed live session."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, session_id):
        tenant, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.generate",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        session = get_object_or_404(
            LiveTranscriptionSession,
            session_id=session_id,
            organization=organization,
        )
        serializer = ClinicalNoteGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            job = TranscriptionService.create_completed_live_job(
                session_id=session.session_id,
                organization_id=organization.id,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=409)

        result = execute_workflow(
            workflow_class=ClinicalNoteGenerateWorkflow,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name="transcription.note.generate",
            payload={
                "job_id": job.job_id,
                "note_type": serializer.validated_data["note_type"],
            },
        )
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return success_response(
            data=GeneratedNoteSerializer(result.data).data,
            request=request,
            status_code=status.HTTP_201_CREATED,
        )


class TranscriptionJobListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.view",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        queryset = TranscriptionJobSelector.queryset(
            organization_id=organization.id,
        )
        return Response(
            TranscriptionJobSerializer(
                queryset,
                many=True,
            ).data
        )

    def post(self, request):
        tenant, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.create",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        serializer = TranscriptionJobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from django.apps import apps as django_apps

        Patient = django_apps.get_model("patient_core", "Patient")
        patient = Patient.objects.get(
            pk=serializer.validated_data["patient"],
        )
        encounter = None
        if serializer.validated_data.get("encounter"):
            from apps.clinical.encounters.models import Encounter

            encounter = Encounter.objects.get(
                pk=serializer.validated_data["encounter"],
            )

        payload = {
            **serializer.validated_data,
            "patient": patient,
            "encounter": encounter,
            "created_by": request.user,
        }

        result = execute_workflow(
            workflow_class=TranscriptionJobCreateWorkflow,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name="transcription.job.create",
            payload=payload,
        )
        if not result.success:
            return Response(
                {"detail": result.message, "code": result.code},
                status=400,
            )
        return Response(
            TranscriptionJobSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class TranscriptionJobDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, job_id):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.view",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        job = TranscriptionJobSelector.get(
            job_id=job_id,
            organization_id=organization.id,
        )
        return Response(TranscriptionJobSerializer(job).data)


class TranscriptionJobActionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    workflow_map = {
        "queue": (
            TranscriptionJobQueueWorkflow,
            "transcription.job.queue",
            "transcription.run",
        ),
        "run": (
            TranscriptionJobRunWorkflow,
            "transcription.job.run",
            "transcription.run",
        ),
        "cancel": (
            TranscriptionJobCancelWorkflow,
            "transcription.job.cancel",
            "transcription.cancel",
        ),
    }

    def post(self, request, job_id, action):
        tenant, organization = require_tenant_organization(request)
        item = self.workflow_map.get(action)
        if item is None:
            return Response({"detail": "Unknown action."}, status=400)

        workflow_class, workflow_name, permission = item
        if not has_permission(
            user=request.user,
            organization=organization,
            permission=permission,
        ):
            return Response({"detail": "Permission denied."}, status=403)

        job = TranscriptionJobSelector.get(
            job_id=job_id,
            organization_id=organization.id,
        )

        result = execute_workflow(
            workflow_class=workflow_class,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name=workflow_name,
            payload={"job_id": job.job_id},
        )
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(TranscriptionJobSerializer(result.data).data)


class GeneratedNoteDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.view",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        note = GeneratedNoteSelector.get(
            note_id=note_id,
            organization_id=organization.id,
        )
        return Response(GeneratedNoteSerializer(note).data)

    def patch(self, request, note_id):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.review",
        ):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = GeneratedNoteUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            note = TranscriptionService.update_note_draft(
                note_id=note_id,
                organization_id=organization.id,
                editor=request.user,
                draft_text=serializer.validated_data["draft_text"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=409)
        return success_response(
            data=GeneratedNoteSerializer(note).data,
            request=request,
        )

    def patch(self, request, note_id):
        _, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.review",
        ):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = GeneratedNoteUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            note = TranscriptionService.update_note_draft(
                note_id=note_id,
                organization_id=organization.id,
                editor=request.user,
                draft_text=serializer.validated_data["draft_text"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=409)
        return success_response(
            data=GeneratedNoteSerializer(note).data,
            request=request,
        )


class GeneratedNoteGenerateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, job_id):
        tenant, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.generate",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        serializer = ClinicalNoteGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = execute_workflow(
            workflow_class=ClinicalNoteGenerateWorkflow,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name="transcription.note.generate",
            payload={
                "job_id": job_id,
                "note_type": serializer.validated_data["note_type"],
            },
        )
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(
            GeneratedNoteSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class GeneratedNoteReviewAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, note_id):
        tenant, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.review",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        serializer = ClinicalNoteReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = execute_workflow(
            workflow_class=ClinicalNoteReviewWorkflow,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name="transcription.note.review",
            payload={
                "note_id": note_id,
                "reviewer": request.user,
                "decision": serializer.validated_data["decision"],
                "rejection_reason": serializer.validated_data.get(
                    "rejection_reason",
                    "",
                ),
            },
        )
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(GeneratedNoteSerializer(result.data).data)


class GeneratedNoteSignAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, note_id):
        tenant, organization = require_tenant_organization(request)
        if not has_permission(
            user=request.user,
            organization=organization,
            permission="transcription.note.sign",
        ):
            return Response({"detail": "Permission denied."}, status=403)

        result = execute_workflow(
            workflow_class=ClinicalNoteSignWorkflow,
            request=request,
            tenant=tenant,
            organization=organization,
            workflow_name="transcription.note.sign",
            payload={
                "note_id": note_id,
                "signer": request.user,
            },
        )
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(GeneratedNoteSerializer(result.data).data)
