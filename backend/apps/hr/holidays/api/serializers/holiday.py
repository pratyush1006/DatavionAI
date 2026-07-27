from rest_framework import serializers

from apps.hr.holidays.models import Holiday

from .fields import (
    HOLIDAY_DETAIL_FIELDS,
    HOLIDAY_LIST_FIELDS,
    HOLIDAY_WRITE_FIELDS,
)


class HolidayBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ()


class HolidayListSerializer(HolidayBaseSerializer):
    class Meta(HolidayBaseSerializer.Meta):
        fields = HOLIDAY_LIST_FIELDS
        read_only_fields = HOLIDAY_LIST_FIELDS


class HolidayDetailSerializer(HolidayBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta(HolidayBaseSerializer.Meta):
        fields = HOLIDAY_DETAIL_FIELDS
        read_only_fields = HOLIDAY_DETAIL_FIELDS


class HolidayCreateSerializer(HolidayBaseSerializer):
    class Meta(HolidayBaseSerializer.Meta):
        fields = HOLIDAY_WRITE_FIELDS


class HolidayUpdateSerializer(HolidayBaseSerializer):
    class Meta(HolidayBaseSerializer.Meta):
        fields = HOLIDAY_WRITE_FIELDS
