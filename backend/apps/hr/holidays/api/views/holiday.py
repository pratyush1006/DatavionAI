"""
API views for holidays.
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
from apps.hr.holidays.api.serializers import (
    HolidayCreateSerializer,
    HolidayDetailSerializer,
    HolidayListSerializer,
    HolidayUpdateSerializer,
)
from apps.hr.holidays.models import Holiday
from apps.hr.holidays.permissions import (
    CanCreateHoliday,
    CanDeleteHoliday,
    CanUpdateHoliday,
    CanViewHoliday,
)
from apps.hr.holidays.selectors import get_holiday_by_id, get_holidays
from apps.hr.holidays.services import (
    create_holiday,
    delete_holiday,
    update_holiday,
)

HOLIDAYS_TAG: Final[tuple[str, ...]] = ("Holidays",)


@extend_schema(tags=HOLIDAYS_TAG)
class HolidayListCreateAPIView(BaseListCreateAPIView):
    """
    List existing holidays or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewHoliday),
        "POST": (IsAuthenticated, CanCreateHoliday),
    }

    serializer_classes = {
        "GET": HolidayListSerializer,
        "POST": HolidayCreateSerializer,
    }

    detail_serializer_class = HolidayDetailSerializer

    create_service = create_holiday

    create_success_message = "Holiday created successfully."

    search_fields = ("name",)

    ordering = ("date",)

    ordering_fields = ("date", "created_at")

    filterset_fields = ("organization", "holiday_type", "is_recurring_yearly")

    def get_queryset(self) -> QuerySet[Holiday]:
        return get_holidays()


@extend_schema(tags=HOLIDAYS_TAG)
class HolidayRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a holiday.
    """

    lookup_url_kwarg = "holiday_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewHoliday),
        "PUT": (IsAuthenticated, CanUpdateHoliday),
        "PATCH": (IsAuthenticated, CanUpdateHoliday),
        "DELETE": (IsAuthenticated, CanDeleteHoliday),
    }

    serializer_classes = {
        "GET": HolidayDetailSerializer,
        "PUT": HolidayUpdateSerializer,
        "PATCH": HolidayUpdateSerializer,
    }

    detail_serializer_class = HolidayDetailSerializer

    update_service = update_holiday

    delete_service = delete_holiday

    update_success_message = "Holiday updated successfully."

    def get_object(self):
        return get_holiday_by_id(
            holiday_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "HolidayListCreateAPIView",
    "HolidayRetrieveUpdateDestroyAPIView",
]
