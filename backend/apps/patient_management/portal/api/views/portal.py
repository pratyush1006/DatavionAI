"""
API views for the Portal Account module.
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
from apps.patient_management.portal.api.serializers import (
    PatientPortalAccountCreateSerializer,
    PatientPortalAccountDetailSerializer,
    PatientPortalAccountListSerializer,
    PatientPortalAccountUpdateSerializer,
)
from apps.patient_management.portal.models import PatientPortalAccount
from apps.patient_management.portal.permissions import (
    CanCreatePatientPortalAccount,
    CanDeletePatientPortalAccount,
    CanUpdatePatientPortalAccount,
    CanViewPatientPortalAccount,
)
from apps.patient_management.portal.selectors import PatientPortalAccountSelector
from apps.patient_management.portal.services import PatientPortalAccountService

TAG: Final[tuple[str, ...]] = ("Patient Portal",)


@extend_schema(tags=TAG)
class PatientPortalAccountListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientPortalAccount),
        "POST": (IsAuthenticated, CanCreatePatientPortalAccount),
    }

    serializer_classes = {
        "GET": PatientPortalAccountListSerializer,
        "POST": PatientPortalAccountCreateSerializer,
    }

    detail_serializer_class = PatientPortalAccountDetailSerializer

    create_service = PatientPortalAccountService.create

    create_success_message = "Portal Account created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("created_at",)
    filterset_fields = ("is_active",)

    def get_queryset(
        self,
    ) -> QuerySet[PatientPortalAccount]:
        return PatientPortalAccountSelector.queryset()


@extend_schema(tags=TAG)
class PatientPortalAccountRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "portal_account_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewPatientPortalAccount),
        "PUT": (IsAuthenticated, CanUpdatePatientPortalAccount),
        "PATCH": (IsAuthenticated, CanUpdatePatientPortalAccount),
        "DELETE": (IsAuthenticated, CanDeletePatientPortalAccount),
    }

    serializer_classes = {
        "GET": PatientPortalAccountDetailSerializer,
        "PUT": PatientPortalAccountUpdateSerializer,
        "PATCH": PatientPortalAccountUpdateSerializer,
    }

    update_service = PatientPortalAccountService.update
    delete_service = PatientPortalAccountService.delete

    def get_object(
        self,
    ) -> PatientPortalAccount:
        return PatientPortalAccountSelector.get(
            portal_account_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PatientPortalAccountListCreateAPIView",
    "PatientPortalAccountRetrieveUpdateDestroyAPIView",
]
