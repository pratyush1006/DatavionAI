"""
API views for the Referral module.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.referrals.api.serializers import (
    PatientReferralCreateSerializer,
    PatientReferralDetailSerializer,
    PatientReferralListSerializer,
    PatientReferralUpdateSerializer,
)
from apps.patient_management.referrals.models import PatientReferral
from apps.patient_management.referrals.permissions import (
    CanCreatePatientReferral,
    CanDeletePatientReferral,
    CanUpdatePatientReferral,
    CanViewPatientReferral,
)
from apps.patient_management.referrals.selectors import PatientReferralSelector
from apps.patient_management.referrals.services import PatientReferralService

TAG: Final[tuple[str, ...]] = ("Referrals",)


@extend_schema(tags=TAG)
class PatientReferralListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientReferral),
        "POST": (IsAuthenticated, CanCreatePatientReferral),
    }

    serializer_classes = {
        "GET": PatientReferralListSerializer,
        "POST": PatientReferralCreateSerializer,
    }

    detail_serializer_class = PatientReferralDetailSerializer

    create_service = PatientReferralService.create

    create_success_message = "Referral created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PatientReferral]:
        return PatientReferralSelector.queryset()


@extend_schema(tags=TAG)
class PatientReferralRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "referral_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientReferral),
        "PUT": (IsAuthenticated, CanUpdatePatientReferral),
        "PATCH": (IsAuthenticated, CanUpdatePatientReferral),
        "DELETE": (IsAuthenticated, CanDeletePatientReferral),
    }

    serializer_classes = {
        "GET": PatientReferralDetailSerializer,
        "PUT": PatientReferralUpdateSerializer,
        "PATCH": PatientReferralUpdateSerializer,
    }

    update_service = PatientReferralService.update
    delete_service = PatientReferralService.delete

    def get_object(
        self,
    ) -> PatientReferral:
        return PatientReferralSelector.get(
            referral_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientReferralListCreateAPIView",
    "PatientReferralRetrieveUpdateDestroyAPIView",
]
