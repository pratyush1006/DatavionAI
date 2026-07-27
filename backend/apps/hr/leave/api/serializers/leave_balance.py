from rest_framework import serializers

from apps.hr.leave.models import LeaveBalance

from .fields import (
    LEAVE_BALANCE_DETAIL_FIELDS,
    LEAVE_BALANCE_LIST_FIELDS,
    LEAVE_BALANCE_WRITE_FIELDS,
)


class LeaveBalanceBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    remaining_days = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = LeaveBalance
        fields = ()

    def get_employee_name(self, obj: LeaveBalance) -> str:
        return obj.employee.full_name


class LeaveBalanceListSerializer(LeaveBalanceBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    leave_type = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )

    class Meta(LeaveBalanceBaseSerializer.Meta):
        fields = LEAVE_BALANCE_LIST_FIELDS
        read_only_fields = LEAVE_BALANCE_LIST_FIELDS


class LeaveBalanceDetailSerializer(LeaveBalanceBaseSerializer):
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

    class Meta(LeaveBalanceBaseSerializer.Meta):
        fields = LEAVE_BALANCE_DETAIL_FIELDS
        read_only_fields = LEAVE_BALANCE_DETAIL_FIELDS


class LeaveBalanceCreateSerializer(LeaveBalanceBaseSerializer):
    class Meta(LeaveBalanceBaseSerializer.Meta):
        fields = LEAVE_BALANCE_WRITE_FIELDS


class LeaveBalanceUpdateSerializer(LeaveBalanceBaseSerializer):
    class Meta(LeaveBalanceBaseSerializer.Meta):
        fields = LEAVE_BALANCE_WRITE_FIELDS
