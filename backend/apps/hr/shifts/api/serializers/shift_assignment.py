from rest_framework import serializers

from apps.hr.shifts.models import ShiftAssignment

from .fields import (
    SHIFT_ASSIGNMENT_DETAIL_FIELDS,
    SHIFT_ASSIGNMENT_LIST_FIELDS,
    SHIFT_ASSIGNMENT_WRITE_FIELDS,
)


class ShiftAssignmentBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = ShiftAssignment
        fields = ()

    def get_employee_name(self, obj: ShiftAssignment) -> str:
        return obj.employee.full_name


class ShiftAssignmentListSerializer(ShiftAssignmentBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    shift = serializers.CharField(
        source="shift.name",
        read_only=True,
    )

    class Meta(ShiftAssignmentBaseSerializer.Meta):
        fields = SHIFT_ASSIGNMENT_LIST_FIELDS
        read_only_fields = SHIFT_ASSIGNMENT_LIST_FIELDS


class ShiftAssignmentDetailSerializer(ShiftAssignmentBaseSerializer):
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

    shift = serializers.CharField(
        source="shift.name",
        read_only=True,
    )

    shift_id = serializers.IntegerField(
        source="shift.id",
        read_only=True,
    )

    class Meta(ShiftAssignmentBaseSerializer.Meta):
        fields = SHIFT_ASSIGNMENT_DETAIL_FIELDS
        read_only_fields = SHIFT_ASSIGNMENT_DETAIL_FIELDS


class ShiftAssignmentCreateSerializer(ShiftAssignmentBaseSerializer):
    class Meta(ShiftAssignmentBaseSerializer.Meta):
        fields = SHIFT_ASSIGNMENT_WRITE_FIELDS


class ShiftAssignmentUpdateSerializer(ShiftAssignmentBaseSerializer):
    class Meta(ShiftAssignmentBaseSerializer.Meta):
        fields = SHIFT_ASSIGNMENT_WRITE_FIELDS
