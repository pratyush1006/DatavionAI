"""
API views for the Patient Profile module.

Architecture:

GET
    API
     |
     v
Selector
     |
     v
PatientProfile

POST
    API
     |
     v
ProfileCreationWorkflow
     |
     v
ProfileService
     |
     v
Domain Event

PUT/PATCH
    API
     |
     v
ProfileUpdateWorkflow
     |
     v
ProfileService
     |
     v
Domain Event

DELETE
    API
     |
     v
ProfileDeletionWorkflow
     |
     v
ProfileService
     |
     v
Domain Event
"""

from __future__ import annotations

from typing import Any, Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

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
from apps.patient_management.profile.models import (
    PatientProfile,
)
from apps.patient_management.profile.permissions import (
    CanCreateProfile,
    CanDeleteProfile,
    CanUpdateProfile,
    CanViewProfile,
)
from apps.patient_management.profile.selectors import (
    ProfileSelector,
)
from apps.patient_management.profile.workflows import (
    ProfileCreationRequest,
    ProfileCreationWorkflow,
    ProfileDeletionRequest,
    ProfileDeletionWorkflow,
    ProfileUpdateRequest,
    ProfileUpdateWorkflow,
)

PROFILE_TAG: Final[tuple[str, ...]] = ("Patient Profile",)


@extend_schema(
    tags=PROFILE_TAG,
)
class ProfileListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create patient profiles.

    GET:
        Selector driven.

    POST:
        Workflow driven.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProfile,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateProfile,
        ),
    }

    serializer_classes = {
        "GET": ProfileListSerializer,
        "POST": ProfileCreateSerializer,
    }

    detail_serializer_class = ProfileDetailSerializer

    create_workflow = ProfileCreationWorkflow

    ordering = ("-created_at",)

    ordering_fields = (
        "preferred_language",
        "created_at",
        "employment_status",
        "education_level",
    )

    filterset_fields = (
        "employment_status",
        "education_level",
        "language_proficiency",
        "is_active",
        "interpreter_required",
    )

    def build_workflow_request(
        self,
        validated_data: dict[str, Any],
    ) -> ProfileCreationRequest:
        """
        Build profile creation workflow request.
        """

        organization = validated_data["organization"]
        patient = validated_data["patient"]

        data = dict(
            validated_data,
        )

        data.pop(
            "organization",
            None,
        )

        data.pop(
            "patient",
            None,
        )

        return ProfileCreationRequest(
            organization_id=organization.id,
            patient_id=patient.id,
            data=data,
        )

    def get_queryset(
        self,
    ) -> QuerySet[PatientProfile]:
        """
        Return profiles visible to the current organization/tenant.
        """

        organization = getattr(
            self,
            "current_organization",
            None,
        )

        if organization is not None:
            return ProfileSelector.list_by_organization(
                organization=organization,
            )

        user = self.current_user

        organization_role = user.organization_roles.select_related(
            "organization",
        ).first()

        if organization_role is None:
            return PatientProfile.objects.none()

        return ProfileSelector.list_by_organization(
            organization=organization_role.organization,
        )

    def resolve_workflow_created_instance(
        self,
        result,
    ):
        """
        Resolve the created PatientProfile from the workflow DTO.
        """

        data = result.data

        if data is None:
            return None

        return self.get_queryset().get(
            id=data.profile_id,
        )


@extend_schema(
    tags=PROFILE_TAG,
)
class ProfileRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a patient profile.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
    """

    lookup_url_kwarg = "profile_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewProfile,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateProfile,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateProfile,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteProfile,
        ),
    }

    serializer_classes = {
        "GET": ProfileDetailSerializer,
        "PUT": ProfileUpdateSerializer,
        "PATCH": ProfileUpdateSerializer,
    }

    detail_serializer_class = ProfileDetailSerializer

    update_workflow = ProfileUpdateWorkflow

    delete_workflow = ProfileDeletionWorkflow

    def get_queryset(
        self,
    ) -> QuerySet[PatientProfile]:
        """
        Return profiles scoped to the current organization.
        """

        organization = getattr(
            self,
            "current_organization",
            None,
        )

        if organization is not None:
            return ProfileSelector.list_by_organization(
                organization=organization,
            )

        user = self.current_user

        organization_role = user.organization_roles.select_related(
            "organization",
        ).first()

        if organization_role is None:
            return PatientProfile.objects.none()

        return ProfileSelector.list_by_organization(
            organization=organization_role.organization,
        )

    def get_object(
        self,
    ) -> PatientProfile:
        """
        Resolve the profile through the selector layer.
        """

        organization = getattr(
            self,
            "current_organization",
            None,
        )

        if organization is not None:
            return ProfileSelector.get(
                profile_id=self.kwargs[self.lookup_url_kwarg],
                organization=organization,
            )

        return ProfileSelector.get(
            profile_id=self.kwargs[self.lookup_url_kwarg],
            tenant_id=self.current_tenant.id,
        )

    def build_update_workflow_request(
        self,
        instance: PatientProfile,
        validated_data: dict[str, Any],
    ) -> ProfileUpdateRequest:
        """
        Build profile update workflow request.
        """

        return ProfileUpdateRequest(
            profile_id=instance.id,
            data=dict(
                validated_data,
            ),
        )

    def build_delete_workflow_request(
        self,
        instance: PatientProfile,
    ) -> ProfileDeletionRequest:
        """
        Build profile deletion workflow request.
        """

        return ProfileDeletionRequest(
            profile_id=instance.id,
        )


__all__ = (
    "ProfileListCreateAPIView",
    "ProfileRetrieveUpdateDestroyAPIView",
)
