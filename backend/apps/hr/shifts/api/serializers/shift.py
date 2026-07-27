from rest_framework import serializers

from apps.hr.shifts.models import Shift

from .fields import (
    SHIFT_DETAIL_FIELDS,
    SHIFT_LIST_FIELDS,
    SHIFT_WRITE_FIELDS,
)


class ShiftBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ()


class ShiftListSerializer(ShiftBaseSerializer):
    class Meta(ShiftBaseSerializer.Meta):
        fields = SHIFT_LIST_FIELDS
        read_only_fields = SHIFT_LIST_FIELDS


class ShiftDetailSerializer(ShiftBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta(ShiftBaseSerializer.Meta):
        fields = SHIFT_DETAIL_FIELDS
        read_only_fields = SHIFT_DETAIL_FIELDS


class ShiftCreateSerializer(ShiftBaseSerializer):
    class Meta(ShiftBaseSerializer.Meta):
        fields = SHIFT_WRITE_FIELDS


class ShiftUpdateSerializer(ShiftBaseSerializer):
    class Meta(ShiftBaseSerializer.Meta):
        fields = SHIFT_WRITE_FIELDS
