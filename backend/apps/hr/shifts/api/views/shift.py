"""
API views for shifts.
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
from apps.hr.shifts.api.serializers import (
    ShiftCreateSerializer,
    ShiftDetailSerializer,
    ShiftListSerializer,
    ShiftUpdateSerializer,
)
from apps.hr.shifts.models import Shift
from apps.hr.shifts.permissions import (
    CanCreateShift,
    CanDeleteShift,
    CanUpdateShift,
    CanViewShift,
)
from apps.hr.shifts.selectors import get_shift_by_id, get_shifts
from apps.hr.shifts.services import create_shift, delete_shift, update_shift

SHIFTS_TAG: Final[tuple[str, ...]] = ("Shifts",)


@extend_schema(tags=SHIFTS_TAG)
class ShiftListCreateAPIView(BaseListCreateAPIView):
    """
    List existing shifts or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewShift),
        "POST": (IsAuthenticated, CanCreateShift),
    }

    serializer_classes = {
        "GET": ShiftListSerializer,
        "POST": ShiftCreateSerializer,
    }

    detail_serializer_class = ShiftDetailSerializer

    create_service = create_shift

    create_success_message = "Shift created successfully."

    search_fields = ("name", "code")

    ordering = ("start_time",)

    ordering_fields = ("start_time", "created_at")

    filterset_fields = ("organization", "is_night_shift", "is_active")

    def get_queryset(self) -> QuerySet[Shift]:
        return get_shifts()


@extend_schema(tags=SHIFTS_TAG)
class ShiftRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a shift.
    """

    lookup_url_kwarg = "shift_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewShift),
        "PUT": (IsAuthenticated, CanUpdateShift),
        "PATCH": (IsAuthenticated, CanUpdateShift),
        "DELETE": (IsAuthenticated, CanDeleteShift),
    }

    serializer_classes = {
        "GET": ShiftDetailSerializer,
        "PUT": ShiftUpdateSerializer,
        "PATCH": ShiftUpdateSerializer,
    }

    detail_serializer_class = ShiftDetailSerializer

    update_service = update_shift

    delete_service = delete_shift

    update_success_message = "Shift updated successfully."

    def get_object(self):
        return get_shift_by_id(shift_id=self.kwargs[self.lookup_url_kwarg])


__all__ = [
    "ShiftListCreateAPIView",
    "ShiftRetrieveUpdateDestroyAPIView",
]
