"""
API views for Patient Relationships.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status

from apps.common.api import BaseAPIView
from apps.common.api.pagination import StandardResultsSetPagination
from apps.common.api.responses import success_response
from apps.patient_management.relationships.api.filters import (
    RelationshipFilter,
)
from apps.patient_management.relationships.api.serializers import (
    RelationshipCreateSerializer,
    RelationshipDetailSerializer,
    RelationshipListSerializer,
    RelationshipUpdateSerializer,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)
from apps.patient_management.relationships.permissions import (
    CanCreateRelationship,
    CanDeleteRelationship,
    CanUpdateRelationship,
    CanViewRelationship,
)


class RelationshipListAPIView(BaseAPIView):
    """
    List patient relationships.
    """

    queryset = PatientRelationship.objects.select_related(
        "organization",
        "patient",
        "related_patient",
    ).all()

    serializer_class = RelationshipListSerializer
    permission_classes = (CanViewRelationship,)
    pagination_class = StandardResultsSetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_class = RelationshipFilter

    search_fields = (
        "relationship_name",
        "patient__first_name",
        "patient__last_name",
        "related_patient__first_name",
        "related_patient__last_name",
    )

    ordering_fields = (
        "relationship_type",
        "created_at",
    )

    ordering = ("-created_at",)


class RelationshipRetrieveAPIView(BaseAPIView):
    """
    Retrieve a patient relationship.
    """

    queryset = PatientRelationship.objects.select_related(
        "organization",
        "patient",
        "related_patient",
    )

    serializer_class = RelationshipDetailSerializer
    permission_classes = (CanViewRelationship,)


class RelationshipCreateAPIView(BaseAPIView):
    """
    Create a patient relationship.
    """

    queryset = PatientRelationship.objects.all()
    serializer_class = RelationshipCreateSerializer
    permission_classes = (CanCreateRelationship,)

    def perform_create(
        self,
        serializer: RelationshipCreateSerializer,
    ) -> None:
        serializer.save()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        response = super().create(
            request,
            *args,
            **kwargs,
        )

        return success_response(
            data=response.data,
            status_code=status.HTTP_201_CREATED,
        )


class RelationshipUpdateAPIView(BaseAPIView):
    """
    Update a patient relationship.
    """

    queryset = PatientRelationship.objects.all()
    serializer_class = RelationshipUpdateSerializer
    permission_classes = (CanUpdateRelationship,)


class RelationshipDestroyAPIView(BaseAPIView):
    """
    Delete a patient relationship.
    """

    queryset = PatientRelationship.objects.all()
    serializer_class = RelationshipDetailSerializer
    permission_classes = (CanDeleteRelationship,)
