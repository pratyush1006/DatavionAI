from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notes.api.serializers import (
    ClinicalNoteAmendmentSerializer,
    ClinicalNoteSerializer,
    ClinicalNoteTemplateSerializer,
)
from apps.notes.models import ClinicalNote, ClinicalNoteTemplate
from apps.notes.permissions.notes import (
    CanAmendNotes,
    CanCreateNotes,
    CanEditNotes,
    CanViewNotes,
)
from apps.notes.services import finalize_signed_note
from apps.notes.workflows import ClinicalNoteAmendmentService, ClinicalNoteService
from apps.platform.rbac.permissions.base import RBACPermissionBase


def _method_permissions(request, mapping):
    """Apply authentication and the RBAC permission for the HTTP method."""
    permission_class = mapping.get(request.method)
    if permission_class is None:
        return [IsAuthenticated()]
    return [IsAuthenticated(), permission_class()]


class NoteActionPermission(RBACPermissionBase):
    """Select a distinct RBAC grant for each note lifecycle transition."""

    action_permissions = {
        "review": "notes.approve",
        "sign": "notes.sign",
        "cancel": "notes.cancel",
    }

    def has_permission(self, request, view):
        self.permission_code = self.action_permissions.get(
            getattr(view, "kwargs", {}).get("action")
        )
        return bool(self.permission_code) and super().has_permission(request, view)


def organization_for(request):
    org = getattr(request, "organization", None)
    if org is None:
        org = getattr(request.user, "organization", None)
    if org is None and getattr(request.user, "organization_id", None):
        from apps.platform.organizations.models import Organization

        org = Organization.objects.filter(pk=request.user.organization_id).first()
    if org is None and request.headers.get("X-Organization-ID"):
        from apps.platform.organizations.models import Organization

        org = Organization.objects.filter(
            pk=request.headers["X-Organization-ID"]
        ).first()
    if org is None:
        raise PermissionDenied("Authenticated user has no active organization.")
    return org


class NoteListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return _method_permissions(
            self.request,
            {"GET": CanViewNotes, "POST": CanCreateNotes},
        )

    def get(self, request):
        org = organization_for(request)
        qs = (
            ClinicalNote.objects.filter(organization=org)
            .select_related("patient", "encounter", "author")
            .order_by("-created_at")
        )
        return Response(ClinicalNoteSerializer(qs, many=True).data)

    def post(self, request):
        org = organization_for(request)
        data = request.data
        from django.apps import apps

        Patient = apps.get_model("patient_core", "Patient")
        patient = Patient.objects.get(pk=data["patient"], organization=org)
        encounter = None
        if data.get("encounter"):
            from apps.clinical.encounters.models import Encounter

            encounter = Encounter.objects.get(pk=data["encounter"], organization=org)
        note = ClinicalNoteService.create(
            organization=org,
            patient=patient,
            author=request.user,
            title=data["title"],
            body=data.get("body", ""),
            note_type=data.get("note_type", "soap"),
            encounter=encounter,
            source=data.get("source", "manual"),
            structured_content=data.get("structured_content", {}),
            metadata=data.get("metadata", {}),
            transcription_job_id=data.get("transcription_job_id"),
            telemedicine_session_id=data.get("telemedicine_session_id"),
        )
        return Response(
            ClinicalNoteSerializer(note).data, status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return _method_permissions(
            self.request,
            {"GET": CanViewNotes, "PATCH": CanEditNotes},
        )

    def get(self, request, note_id):
        org = organization_for(request)
        note = ClinicalNote.objects.get(note_id=note_id, organization=org)
        return Response(ClinicalNoteSerializer(note).data)

    def patch(self, request, note_id):
        org = organization_for(request)
        note = ClinicalNoteService.update_draft(
            note_id=note_id,
            organization_id=org.id,
            actor=request.user,
            title=request.data.get("title"),
            body=request.data.get("body"),
            structured_content=request.data.get("structured_content"),
            reason=request.data.get("reason", ""),
        )
        return Response(ClinicalNoteSerializer(note).data)


class NoteActionAPIView(APIView):
    permission_classes = [IsAuthenticated, NoteActionPermission]

    def post(self, request, note_id, action):
        org = organization_for(request)
        note = ClinicalNote.objects.get(note_id=note_id, organization=org)
        if action == "review":
            note = ClinicalNoteService.submit_for_review(
                note_id=note.note_id, organization_id=org.id, actor=request.user
            )
        elif action == "sign":
            note = ClinicalNoteService.sign(
                note_id=note.note_id, organization_id=org.id, actor=request.user
            )
            finalize_signed_note(note=note)
        elif action == "cancel":
            note = ClinicalNoteService.cancel(
                note_id=note.note_id,
                organization_id=org.id,
                actor=request.user,
                reason=request.data.get("reason", ""),
            )
        else:
            return Response({"detail": "Unsupported action."}, status=400)
        return Response(ClinicalNoteSerializer(note).data)


class NoteAmendmentAPIView(APIView):
    permission_classes = [IsAuthenticated, CanAmendNotes]

    def post(self, request, note_id):
        org = organization_for(request)
        note = ClinicalNote.objects.get(note_id=note_id, organization=org)
        amendment = ClinicalNoteAmendmentService.request(
            note=note,
            actor=request.user,
            reason=request.data["reason"],
            proposed_body=request.data["proposed_body"],
            proposed_structured_content=request.data.get(
                "proposed_structured_content", {}
            ),
        )
        return Response(ClinicalNoteAmendmentSerializer(amendment).data, status=201)


class NoteTemplateListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return _method_permissions(
            self.request,
            {"GET": CanViewNotes, "POST": CanEditNotes},
        )

    def get(self, request):
        org = organization_for(request)
        return Response(
            ClinicalNoteTemplateSerializer(
                ClinicalNoteTemplate.objects.filter(organization=org, is_active=True),
                many=True,
            ).data
        )

    def post(self, request):
        org = organization_for(request)
        template = ClinicalNoteTemplate.objects.create(
            organization=org,
            name=request.data["name"],
            note_type=request.data.get("note_type", "soap"),
            schema=request.data.get("schema", {}),
            default_content=request.data.get("default_content", {}),
            is_system=False,
        )
        return Response(ClinicalNoteTemplateSerializer(template).data, status=201)
