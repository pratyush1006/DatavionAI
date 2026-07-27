"""
API views for lifecycle processes.
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
from apps.hr.onboarding.api.serializers import (
    LifecycleProcessCreateSerializer,
    LifecycleProcessDetailSerializer,
    LifecycleProcessListSerializer,
    LifecycleProcessUpdateSerializer,
)
from apps.hr.onboarding.models import LifecycleProcess
from apps.hr.onboarding.permissions import (
    CanCreateLifecycleProcess,
    CanDeleteLifecycleProcess,
    CanUpdateLifecycleProcess,
    CanViewLifecycleProcess,
)
from apps.hr.onboarding.selectors import (
    get_lifecycle_process_by_id,
    get_lifecycle_processes,
)
from apps.hr.onboarding.services import (
    delete_lifecycle_process,
    start_lifecycle_process,
    update_lifecycle_process,
)

ONBOARDING_TAG: Final[tuple[str, ...]] = ("Onboarding",)


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleProcessListCreateAPIView(BaseListCreateAPIView):
    """
    List existing lifecycle processes or start a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLifecycleProcess),
        "POST": (IsAuthenticated, CanCreateLifecycleProcess),
    }

    serializer_classes = {
        "GET": LifecycleProcessListSerializer,
        "POST": LifecycleProcessCreateSerializer,
    }

    detail_serializer_class = LifecycleProcessDetailSerializer

    create_service = start_lifecycle_process

    create_success_message = "Lifecycle process started successfully."

    search_fields = ("employee__employee_code",)

    ordering = ("-start_date",)

    ordering_fields = ("start_date", "created_at")

    filterset_fields = (
        "organization",
        "employee",
        "process_type",
        "status",
    )

    def get_queryset(self) -> QuerySet[LifecycleProcess]:
        return get_lifecycle_processes()


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleProcessRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a lifecycle process.
    """

    lookup_url_kwarg = "lifecycle_process_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLifecycleProcess),
        "PUT": (IsAuthenticated, CanUpdateLifecycleProcess),
        "PATCH": (IsAuthenticated, CanUpdateLifecycleProcess),
        "DELETE": (IsAuthenticated, CanDeleteLifecycleProcess),
    }

    serializer_classes = {
        "GET": LifecycleProcessDetailSerializer,
        "PUT": LifecycleProcessUpdateSerializer,
        "PATCH": LifecycleProcessUpdateSerializer,
    }

    detail_serializer_class = LifecycleProcessDetailSerializer

    update_service = update_lifecycle_process

    delete_service = delete_lifecycle_process

    update_success_message = "Lifecycle process updated successfully."

    def get_object(self):
        return get_lifecycle_process_by_id(
            lifecycle_process_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LifecycleProcessListCreateAPIView",
    "LifecycleProcessRetrieveUpdateDestroyAPIView",
]
