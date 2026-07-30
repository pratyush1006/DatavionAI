"""
API views for clinical notes and templates.
"""

from __future__ import annotations

from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.common.api.responses import error_response, success_response
from apps.notes.api.serializers import (
    NoteCreateSerializer,
    NoteDetailSerializer,
    NoteListSerializer,
    TemplateCreateSerializer,
    TemplateDetailSerializer,
    TemplateListSerializer,
    TemplateUpdateSerializer,
)
from apps.notes.permissions import (
    CanAmendNote,
    CanCreateNote,
    CanDeleteNote,
    CanSignNote,
    CanUpdateNote,
    CanViewNote,
)
from apps.notes.selectors import NoteSelector, TemplateSelector
from apps.notes.services import NoteService, TemplateService
from apps.organization.employees.models import Employee

NOTE_TAG: Final[tuple[str, ...]] = ("Clinical Notes",)


# -------------------------------------------------------------------------
# Template Views
# -------------------------------------------------------------------------


@extend_schema(tags=NOTE_TAG)
class NoteTemplateListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing note templates and creating new note templates.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewNote,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateNote,
        ),
    }

    serializer_classes = {
        "GET": TemplateListSerializer,
        "POST": TemplateCreateSerializer,
    }

    detail_serializer_class = TemplateDetailSerializer

    create_service = TemplateService.create

    create_success_message = "Note template created successfully."

    search_fields = ("name",)

    ordering = ("name",)

    ordering_fields = (
        "name",
        "template_type",
        "is_active",
    )

    filterset_fields = (
        "template_type",
        "is_active",
        "is_system_template",
    )

    def get_queryset(
        self,
    ) -> Any:
        """
        Return the note template queryset.
        """

        return TemplateSelector.queryset()


@extend_schema(tags=NOTE_TAG)
class NoteTemplateRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, or delete a note template.
    """

    permission_classes = (
        IsAuthenticated,
        CanViewNote,
    )

    def get(
        self,
        request: Request,
        *,
        template_id: Any,
    ) -> Response:
        """
        Retrieve a note template.
        """

        template = TemplateSelector.get(
            template_id=template_id,
        )

        serializer = TemplateDetailSerializer(
            template,
        )

        return success_response(
            data=serializer.data,
        )

    def put(
        self,
        request: Request,
        *,
        template_id: Any,
    ) -> Response:
        """
        Update a note template.
        """

        template = TemplateSelector.get(
            template_id=template_id,
        )

        serializer = TemplateUpdateSerializer(
            template,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated_template = TemplateService.update(
            instance=template,
            validated_data=serializer.validated_data,
        )

        response_serializer = TemplateDetailSerializer(
            updated_template,
        )

        return success_response(
            message="Note template updated successfully.",
            data=response_serializer.data,
        )

    def patch(
        self,
        request: Request,
        *,
        template_id: Any,
    ) -> Response:
        """
        Partially update a note template.
        """

        template = TemplateSelector.get(
            template_id=template_id,
        )

        serializer = TemplateUpdateSerializer(
            template,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated_template = TemplateService.update(
            instance=template,
            validated_data=serializer.validated_data,
        )

        response_serializer = TemplateDetailSerializer(
            updated_template,
        )

        return success_response(
            message="Note template updated successfully.",
            data=response_serializer.data,
        )

    def delete(
        self,
        request: Request,
        *,
        template_id: Any,
    ) -> Response:
        """
        Delete a note template.
        """

        template = TemplateSelector.get(
            template_id=template_id,
        )

        template.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# -------------------------------------------------------------------------
# Note Views
# -------------------------------------------------------------------------


@extend_schema(tags=NOTE_TAG)
class NoteListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing clinical notes and creating new clinical notes.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewNote,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateNote,
        ),
    }

    serializer_classes = {
        "GET": NoteListSerializer,
        "POST": NoteCreateSerializer,
    }

    detail_serializer_class = NoteDetailSerializer

    create_service = NoteService.create

    create_success_message = "Clinical note created successfully."

    search_fields = (
        "title",
        "raw_text",
    )

    ordering = ("-created_at",)

    ordering_fields = (
        "title",
        "created_at",
        "note_type",
    )

    filterset_fields = (
        "note_type",
        "is_amended",
        "created_by",
    )

    def get_queryset(
        self,
    ) -> Any:
        """
        Return the clinical note queryset.
        """

        patient_id = self.kwargs.get("patient_id")
        encounter_id = self.kwargs.get("encounter_id")

        queryset = NoteSelector.queryset()

        if patient_id:
            return NoteSelector.list_by_patient(
                patient_id=patient_id,
            )

        if encounter_id:
            return NoteSelector.list_by_encounter(
                encounter_id=encounter_id,
            )

        return queryset


@extend_schema(tags=NOTE_TAG)
class NoteRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, delete, sign, or amend a clinical note.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewNote,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateNote,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateNote,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteNote,
        ),
        "POST": (IsAuthenticated,),
    }

    def _get_employee(
        self,
        request: Request,
    ) -> Employee | None:
        """
        Return the employee associated with the authenticated user.
        """

        try:
            return Employee.objects.get(
                user=request.user,
            )
        except Employee.DoesNotExist:
            return None

    def get_permissions(
        self,
    ) -> list[Any]:
        """
        Return permissions for the current request.
        """

        method = self.request.method

        if method == "POST":
            action = self.request.path.rstrip("/").split("/")[-1]

            if action == "sign":
                return [
                    permission()
                    for permission in (
                        IsAuthenticated,
                        CanSignNote,
                    )
                ]

            if action == "amend":
                return [
                    permission()
                    for permission in (
                        IsAuthenticated,
                        CanAmendNote,
                    )
                ]

        return super().get_permissions()

    def get(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Retrieve a clinical note.
        """

        note = NoteSelector.get(
            note_id=note_id,
        )

        serializer = NoteDetailSerializer(
            note,
        )

        return success_response(
            data=serializer.data,
        )

    def put(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Update a clinical note.
        """

        note = NoteSelector.get(
            note_id=note_id,
        )

        serializer = NoteDetailSerializer(
            note,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated_note = NoteService.update(
            instance=note,
            validated_data=serializer.validated_data,
        )

        response_serializer = NoteDetailSerializer(
            updated_note,
        )

        return success_response(
            message="Clinical note updated successfully.",
            data=response_serializer.data,
        )

    def patch(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Partially update a clinical note.
        """

        note = NoteSelector.get(
            note_id=note_id,
        )

        serializer = NoteDetailSerializer(
            note,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        updated_note = NoteService.update(
            instance=note,
            validated_data=serializer.validated_data,
        )

        response_serializer = NoteDetailSerializer(
            updated_note,
        )

        return success_response(
            message="Clinical note updated successfully.",
            data=response_serializer.data,
        )

    def delete(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Delete a clinical note.
        """

        note = NoteSelector.get(
            note_id=note_id,
        )

        note.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        tags=NOTE_TAG,
        description="Sign a clinical note.",
    )
    def post_sign(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Sign a clinical note.
        """

        employee = self._get_employee(
            request,
        )

        if employee is None:
            return error_response(
                message="Employee profile not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        signed_note = NoteService.sign(
            note_id=note_id,
            signed_by=employee,
        )

        serializer = NoteDetailSerializer(
            signed_note,
        )

        return success_response(
            message="Clinical note signed successfully.",
            data=serializer.data,
        )

    @extend_schema(
        tags=NOTE_TAG,
        description="Amend a clinical note.",
    )
    def post_amend(
        self,
        request: Request,
        *,
        note_id: Any,
    ) -> Response:
        """
        Amend a clinical note by creating a new version.
        """

        employee = self._get_employee(
            request,
        )

        if employee is None:
            return error_response(
                message="Employee profile not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        amendment_reason = request.data.get(
            "amendment_reason",
            "",
        )

        updated_content = request.data.get(
            "content",
            {},
        )

        amended_note = NoteService.amend(
            note_id=note_id,
            amendment_reason=amendment_reason,
            updated_content=updated_content,
            amended_by=employee,
        )

        serializer = NoteDetailSerializer(
            amended_note,
        )

        return success_response(
            message="Clinical note amended successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class NoteBulkCreateAPIView(APIView):
    """
    Bulk create clinical notes.
    """

    permission_classes = (IsAuthenticated, CanCreateNote)

    serializer_class = NoteCreateSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple clinical notes.
        """

        serializer = self.serializer_class(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        notes = NoteService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = NoteDetailSerializer(
            notes,
            many=True,
        )

        return success_response(
            message="Clinical notes created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


__all__ = [
    "NoteBulkCreateAPIView",
    "NoteListCreateAPIView",
    "NoteRetrieveUpdateDestroyAPIView",
    "NoteTemplateListCreateAPIView",
    "NoteTemplateRetrieveUpdateDestroyAPIView",
]
