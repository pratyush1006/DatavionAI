"""
API views for lifecycle tasks.
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
    LifecycleTaskSerializer,
    LifecycleTaskWriteSerializer,
)
from apps.hr.onboarding.models import LifecycleTask
from apps.hr.onboarding.permissions import (
    CanCreateLifecycleTask,
    CanDeleteLifecycleTask,
    CanUpdateLifecycleTask,
    CanViewLifecycleTask,
)
from apps.hr.onboarding.selectors import (
    get_lifecycle_task_by_id,
    get_lifecycle_tasks,
)
from apps.hr.onboarding.services import (
    create_lifecycle_task,
    delete_lifecycle_task,
    update_lifecycle_task,
)

ONBOARDING_TAG: Final[tuple[str, ...]] = ("Onboarding",)


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleTaskListCreateAPIView(BaseListCreateAPIView):
    """
    List existing lifecycle tasks or add an ad-hoc one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLifecycleTask),
        "POST": (IsAuthenticated, CanCreateLifecycleTask),
    }

    serializer_classes = {
        "GET": LifecycleTaskSerializer,
        "POST": LifecycleTaskWriteSerializer,
    }

    detail_serializer_class = LifecycleTaskSerializer

    create_service = create_lifecycle_task

    create_success_message = "Task added successfully."

    search_fields = ("title",)

    ordering = ("order",)

    ordering_fields = ("order", "due_date", "created_at")

    filterset_fields = ("process", "status", "category", "assigned_to")

    def get_queryset(self) -> QuerySet[LifecycleTask]:
        return get_lifecycle_tasks()


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleTaskRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a lifecycle task.
    """

    lookup_url_kwarg = "lifecycle_task_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewLifecycleTask),
        "PUT": (IsAuthenticated, CanUpdateLifecycleTask),
        "PATCH": (IsAuthenticated, CanUpdateLifecycleTask),
        "DELETE": (IsAuthenticated, CanDeleteLifecycleTask),
    }

    serializer_classes = {
        "GET": LifecycleTaskSerializer,
        "PUT": LifecycleTaskWriteSerializer,
        "PATCH": LifecycleTaskWriteSerializer,
    }

    detail_serializer_class = LifecycleTaskSerializer

    update_service = update_lifecycle_task

    delete_service = delete_lifecycle_task

    update_success_message = "Task updated successfully."

    def get_object(self):
        return get_lifecycle_task_by_id(
            lifecycle_task_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LifecycleTaskListCreateAPIView",
    "LifecycleTaskRetrieveUpdateDestroyAPIView",
]
