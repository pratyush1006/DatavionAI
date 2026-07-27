"""
Study serializers for the Imaging application.
"""

from __future__ import annotations

from apps.imaging.api.serializers.fields import (
    DETAIL_FIELDS,
    LIST_FIELDS,
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
    WRITE_FIELDS,
)
from apps.imaging.models import Study
from apps.imaging.services import StudyService


class StudyBaseSerializer:
    """
    Base serializer mixin for Study serializers.
    """

    class Meta:
        model = Study
        fields = ()


class StudySerializer(
    StudyBaseSerializer,
):
    """
    Generic Study serializer.
    """

    class Meta(
        StudyBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "organization",
            "patient",
            "study_instance_uid",
            "accession_number",
            "study_date",
            "modality",
            "study_description",
            "referring_physician",
            "status",
            "created_at",
            "updated_at",
        )


class StudyCreateSerializer(
    StudyBaseSerializer,
):
    """
    Serializer used for creating imaging studies.
    """

    class Meta(
        StudyBaseSerializer.Meta,
    ):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create an imaging study.
        """

        return StudyService.create(
            validated_data=validated_data,
        )


class StudyUpdateSerializer(
    StudyBaseSerializer,
):
    """
    Serializer used for updating imaging studies.
    """

    class Meta(
        StudyBaseSerializer.Meta,
    ):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Study,
        validated_data: dict[str, object],
    ) -> Study:
        """
        Update an imaging study.
        """

        return StudyService.update(
            instance=instance,
            validated_data=validated_data,
        )


class StudyListSerializer(
    StudyBaseSerializer,
):
    """
    Serializer used for listing imaging studies.
    """

    class Meta(
        StudyBaseSerializer.Meta,
    ):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class StudyDetailSerializer(
    StudyBaseSerializer,
):
    """
    Serializer used for retrieving imaging study details.
    """

    class Meta(
        StudyBaseSerializer.Meta,
    ):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "StudyCreateSerializer",
    "StudyDetailSerializer",
    "StudyListSerializer",
    "StudySerializer",
    "StudyUpdateSerializer",
]
