from rest_framework import serializers

from apps.hr.leave.models import LeaveRequest

from .fields import (
    LEAVE_REQUEST_DECISION_FIELDS,
    LEAVE_REQUEST_DETAIL_FIELDS,
    LEAVE_REQUEST_LIST_FIELDS,
    LEAVE_REQUEST_WRITE_FIELDS,
)


class LeaveRequestBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = ()

    def get_employee_name(self, obj: LeaveRequest) -> str:
        return obj.employee.full_name


class LeaveRequestListSerializer(LeaveRequestBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    leave_type = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )

    class Meta(LeaveRequestBaseSerializer.Meta):
        fields = LEAVE_REQUEST_LIST_FIELDS
        read_only_fields = LEAVE_REQUEST_LIST_FIELDS


class LeaveRequestDetailSerializer(LeaveRequestBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    employee_id = serializers.IntegerField(
        source="employee.id",
        read_only=True,
    )

    leave_type = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )

    leave_type_id = serializers.IntegerField(
        source="leave_type.id",
        read_only=True,
    )

    approver = serializers.SerializerMethodField()

    approver_id = serializers.IntegerField(
        source="approver.id",
        read_only=True,
    )

    class Meta(LeaveRequestBaseSerializer.Meta):
        fields = LEAVE_REQUEST_DETAIL_FIELDS
        read_only_fields = LEAVE_REQUEST_DETAIL_FIELDS

    def get_approver(self, obj: LeaveRequest):
        if obj.approver:
            return obj.approver.full_name
        return None


class LeaveRequestCreateSerializer(LeaveRequestBaseSerializer):
    class Meta(LeaveRequestBaseSerializer.Meta):
        fields = LEAVE_REQUEST_WRITE_FIELDS


class LeaveRequestUpdateSerializer(LeaveRequestBaseSerializer):
    class Meta(LeaveRequestBaseSerializer.Meta):
        fields = LEAVE_REQUEST_WRITE_FIELDS


class LeaveRequestDecisionSerializer(LeaveRequestBaseSerializer):
    class Meta(LeaveRequestBaseSerializer.Meta):
        fields = LEAVE_REQUEST_DECISION_FIELDS
