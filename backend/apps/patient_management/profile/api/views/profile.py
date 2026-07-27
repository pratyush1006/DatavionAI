"""
API views for the Patient Profile module.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.profile.api.serializers import (
    ProfileCreateSerializer,
    ProfileDetailSerializer,
    ProfileListSerializer,
    ProfileUpdateSerializer,
)
from apps.patient_management.profile.models import PatientProfile
from apps.patient_management.profile.permissions import (
    CanCreateProfile,
    CanDeleteProfile,
    CanUpdateProfile,
    CanViewProfile,
)
from apps.patient_management.profile.selectors import ProfileSelector
from apps.patient_management.profile.services import ProfileService
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

PROFILE_TAG: Final[tuple[str, ...]] = ("Patient Profile",)


@extend_schema(tags=PROFILE_TAG)
class ProfileListCreateAPIView(BaseListCreateAPIView):
    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewProfile),
        "POST": (IsAuthenticated, CanCreateProfile),
    }

    serializer_classes = {
        "GET": ProfileListSerializer,
        "POST": ProfileCreateSerializer,
    }

    detail_serializer_class = ProfileDetailSerializer

    create_service = ProfileService.create

    create_success_message = "Patient profile created successfully."

    ordering = ("-created_at",)
    ordering_fields = ("preferred_language", "created_at")
    filterset_fields = (
        "employment_status",
        "education_level",
        "language_proficiency",
        "is_active",
    )

    def get_queryset(
        self,
    ) -> QuerySet[PatientProfile]:
        return ProfileSelector.queryset()


@extend_schema(tags=PROFILE_TAG)
class ProfileRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    lookup_url_kwarg = "profile_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewProfile),
        "PUT": (IsAuthenticated, CanUpdateProfile),
        "PATCH": (IsAuthenticated, CanUpdateProfile),
        "DELETE": (IsAuthenticated, CanDeleteProfile),
    }

    serializer_classes = {
        "GET": ProfileDetailSerializer,
        "PUT": ProfileUpdateSerializer,
        "PATCH": ProfileUpdateSerializer,
    }

    update_service = ProfileService.update
    delete_service = ProfileService.delete

    def get_object(
        self,
    ) -> PatientProfile:
        return ProfileSelector.get(
            profile_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "ProfileListCreateAPIView",
    "ProfileRetrieveUpdateDestroyAPIView",
]
