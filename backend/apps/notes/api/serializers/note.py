"""
Serializers for the Notes application.
"""

from __future__ import annotations

from apps.notes.api.serializers.base import (
    NoteBaseSerializer,
    TemplateBaseSerializer,
)
from apps.notes.api.serializers.fields import (
    DETAIL_FIELDS,
    LIST_FIELDS,
    NOTE_DETAIL_FIELDS,
    NOTE_LIST_FIELDS,
    NOTE_READ_ONLY_FIELDS,
    NOTE_UPDATE_FIELDS,
    NOTE_WRITE_FIELDS,
    READ_ONLY_FIELDS,
    TEMPLATE_UPDATE_FIELDS,
    TEMPLATE_WRITE_FIELDS,
)
from apps.notes.models import ClinicalNote, NoteTemplate
from apps.notes.services import NoteService, TemplateService

# -------------------------------------------------------------------------
# Template Serializers
# -------------------------------------------------------------------------


class TemplateListSerializer(TemplateBaseSerializer):
    """
    Serializer used for listing note templates.
    """

    class Meta(TemplateBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class TemplateDetailSerializer(TemplateBaseSerializer):
    """
    Serializer used for retrieving note template details.
    """

    class Meta(TemplateBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class TemplateCreateSerializer(TemplateBaseSerializer):
    """
    Serializer used for creating note templates.
    """

    class Meta(TemplateBaseSerializer.Meta):
        fields = TEMPLATE_WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ) -> NoteTemplate:
        """
        Create a note template.
        """

        return TemplateService.create(
            validated_data=validated_data,
        )


class TemplateUpdateSerializer(TemplateBaseSerializer):
    """
    Serializer used for updating note templates.
    """

    class Meta(TemplateBaseSerializer.Meta):
        fields = TEMPLATE_UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: NoteTemplate,
        validated_data: dict[str, object],
    ) -> NoteTemplate:
        """
        Update a note template.
        """

        return TemplateService.update(
            instance=instance,
            validated_data=validated_data,
        )


# -------------------------------------------------------------------------
# Note Serializers
# -------------------------------------------------------------------------


class NoteListSerializer(NoteBaseSerializer):
    """
    Serializer used for listing clinical notes.
    """

    class Meta(NoteBaseSerializer.Meta):
        fields = NOTE_LIST_FIELDS
        read_only_fields = NOTE_READ_ONLY_FIELDS


class NoteDetailSerializer(NoteBaseSerializer):
    """
    Serializer used for retrieving clinical note details.
    """

    class Meta(NoteBaseSerializer.Meta):
        fields = NOTE_DETAIL_FIELDS
        read_only_fields = NOTE_READ_ONLY_FIELDS


class NoteCreateSerializer(NoteBaseSerializer):
    """
    Serializer used for creating clinical notes.
    """

    class Meta(NoteBaseSerializer.Meta):
        fields = NOTE_WRITE_FIELDS
        read_only_fields = NOTE_READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ) -> ClinicalNote:
        """
        Create a clinical note.
        """

        return NoteService.create(
            validated_data=validated_data,
        )


class NoteUpdateSerializer(NoteBaseSerializer):
    """
    Serializer used for updating clinical notes.
    """

    class Meta(NoteBaseSerializer.Meta):
        fields = NOTE_UPDATE_FIELDS
        read_only_fields = NOTE_READ_ONLY_FIELDS

    def update(
        self,
        instance: ClinicalNote,
        validated_data: dict[str, object],
    ) -> ClinicalNote:
        """
        Update a clinical note.
        """

        return NoteService.update(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "NoteCreateSerializer",
    "NoteDetailSerializer",
    "NoteListSerializer",
    "NoteUpdateSerializer",
    "TemplateCreateSerializer",
    "TemplateDetailSerializer",
    "TemplateListSerializer",
    "TemplateUpdateSerializer",
]
