"""
API views for Patient Consents.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.common.api import BaseAPIView
from apps.common.api.pagination import (
    StandardResultsSetPagination,
)
from apps.patient_management.consents.api.filters import (
    ConsentFilter,
)
from apps.patient_management.consents.api.serializers import (
    ConsentCreateSerializer,
    ConsentDetailSerializer,
    ConsentListSerializer,
    ConsentUpdateSerializer,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)
from apps.patient_management.consents.permissions import (
    CanCreateConsent,
    CanDeleteConsent,
    CanUpdateConsent,
    CanViewConsent,
)


class ConsentListAPIView(BaseAPIView):
    """
    List patient consents.
    """

    queryset = PatientConsent.objects.select_related(
        "organization",
        "patient",
    ).all()

    serializer_class = ConsentListSerializer

    permission_classes = (CanViewConsent,)

    pagination_class = StandardResultsSetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_class = ConsentFilter

    search_fields = (
        "granted_by",
        "patient__first_name",
        "patient__last_name",
    )

    ordering_fields = (
        "effective_at",
        "expires_at",
        "created_at",
    )

    ordering = ("-effective_at",)


class ConsentRetrieveAPIView(
    BaseAPIView,
):
    """
    Retrieve a consent.
    """

    queryset = PatientConsent.objects.select_related(
        "organization",
        "patient",
    )

    serializer_class = ConsentDetailSerializer

    permission_classes = (CanViewConsent,)


class ConsentCreateAPIView(
    BaseAPIView,
):
    """
    Create a consent.
    """

    queryset = PatientConsent.objects.all()

    serializer_class = ConsentCreateSerializer

    permission_classes = (CanCreateConsent,)


class ConsentUpdateAPIView(
    BaseAPIView,
):
    """
    Update a consent.
    """

    queryset = PatientConsent.objects.all()

    serializer_class = ConsentUpdateSerializer

    permission_classes = (CanUpdateConsent,)


class ConsentDestroyAPIView(
    BaseAPIView,
):
    """
    Delete a consent.
    """

    queryset = PatientConsent.objects.all()

    serializer_class = ConsentDetailSerializer

    permission_classes = (CanDeleteConsent,)
