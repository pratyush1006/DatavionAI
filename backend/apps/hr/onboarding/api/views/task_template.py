"""
API views for lifecycle task templates.
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
    LifecycleTaskTemplateCreateSerializer,
    LifecycleTaskTemplateDetailSerializer,
    LifecycleTaskTemplateListSerializer,
    LifecycleTaskTemplateUpdateSerializer,
)
from apps.hr.onboarding.models import LifecycleTaskTemplate
from apps.hr.onboarding.permissions import (
    CanCreateTaskTemplate,
    CanDeleteTaskTemplate,
    CanUpdateTaskTemplate,
    CanViewTaskTemplate,
)
from apps.hr.onboarding.selectors import (
    get_task_template_by_id,
    get_task_templates,
)
from apps.hr.onboarding.services import (
    create_task_template,
    delete_task_template,
    update_task_template,
)

ONBOARDING_TAG: Final[tuple[str, ...]] = ("Onboarding",)


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleTaskTemplateListCreateAPIView(BaseListCreateAPIView):
    """
    List existing lifecycle task templates or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewTaskTemplate),
        "POST": (IsAuthenticated, CanCreateTaskTemplate),
    }

    serializer_classes = {
        "GET": LifecycleTaskTemplateListSerializer,
        "POST": LifecycleTaskTemplateCreateSerializer,
    }

    detail_serializer_class = LifecycleTaskTemplateDetailSerializer

    create_service = create_task_template

    create_success_message = "Task template created successfully."

    search_fields = ("title",)

    ordering = ("process_type", "order")

    ordering_fields = ("order", "created_at")

    filterset_fields = ("organization", "process_type", "category", "is_active")

    def get_queryset(self) -> QuerySet[LifecycleTaskTemplate]:
        return get_task_templates()


@extend_schema(tags=ONBOARDING_TAG)
class LifecycleTaskTemplateRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a lifecycle task template.
    """

    lookup_url_kwarg = "task_template_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewTaskTemplate),
        "PUT": (IsAuthenticated, CanUpdateTaskTemplate),
        "PATCH": (IsAuthenticated, CanUpdateTaskTemplate),
        "DELETE": (IsAuthenticated, CanDeleteTaskTemplate),
    }

    serializer_classes = {
        "GET": LifecycleTaskTemplateDetailSerializer,
        "PUT": LifecycleTaskTemplateUpdateSerializer,
        "PATCH": LifecycleTaskTemplateUpdateSerializer,
    }

    detail_serializer_class = LifecycleTaskTemplateDetailSerializer

    update_service = update_task_template

    delete_service = delete_task_template

    update_success_message = "Task template updated successfully."

    def get_object(self):
        return get_task_template_by_id(
            task_template_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "LifecycleTaskTemplateListCreateAPIView",
    "LifecycleTaskTemplateRetrieveUpdateDestroyAPIView",
]
