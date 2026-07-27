from rest_framework import serializers

from apps.hr.leave.models import LeaveType

from .fields import (
    LEAVE_TYPE_DETAIL_FIELDS,
    LEAVE_TYPE_LIST_FIELDS,
    LEAVE_TYPE_WRITE_FIELDS,
)


class LeaveTypeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ()


class LeaveTypeListSerializer(LeaveTypeBaseSerializer):
    class Meta(LeaveTypeBaseSerializer.Meta):
        fields = LEAVE_TYPE_LIST_FIELDS
        read_only_fields = LEAVE_TYPE_LIST_FIELDS


class LeaveTypeDetailSerializer(LeaveTypeBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta(LeaveTypeBaseSerializer.Meta):
        fields = LEAVE_TYPE_DETAIL_FIELDS
        read_only_fields = LEAVE_TYPE_DETAIL_FIELDS


class LeaveTypeCreateSerializer(LeaveTypeBaseSerializer):
    class Meta(LeaveTypeBaseSerializer.Meta):
        fields = LEAVE_TYPE_WRITE_FIELDS


class LeaveTypeUpdateSerializer(LeaveTypeBaseSerializer):
    class Meta(LeaveTypeBaseSerializer.Meta):
        fields = LEAVE_TYPE_WRITE_FIELDS
