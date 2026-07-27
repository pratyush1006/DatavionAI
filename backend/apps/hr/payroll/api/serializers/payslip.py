from rest_framework import serializers

from apps.hr.payroll.models import Payslip

from .fields import (
    PAYSLIP_DETAIL_FIELDS,
    PAYSLIP_LIST_FIELDS,
    PAYSLIP_WRITE_FIELDS,
)
from .payslip_line_item import (
    PayslipLineItemInputSerializer,
    PayslipLineItemOutputSerializer,
)


class PayslipBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Payslip
        fields = ()

    def get_employee_name(self, obj: Payslip) -> str:
        return obj.employee.full_name


class PayslipListSerializer(PayslipBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    class Meta(PayslipBaseSerializer.Meta):
        fields = PAYSLIP_LIST_FIELDS
        read_only_fields = PAYSLIP_LIST_FIELDS


class PayslipDetailSerializer(PayslipBaseSerializer):
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

    line_items = PayslipLineItemOutputSerializer(
        many=True,
        read_only=True,
    )

    class Meta(PayslipBaseSerializer.Meta):
        fields = PAYSLIP_DETAIL_FIELDS
        read_only_fields = PAYSLIP_DETAIL_FIELDS


class PayslipCreateSerializer(PayslipBaseSerializer):
    line_items = PayslipLineItemInputSerializer(
        many=True,
        required=False,
    )

    class Meta(PayslipBaseSerializer.Meta):
        fields = PAYSLIP_WRITE_FIELDS


class PayslipUpdateSerializer(PayslipBaseSerializer):
    line_items = PayslipLineItemInputSerializer(
        many=True,
        required=False,
    )

    class Meta(PayslipBaseSerializer.Meta):
        fields = PAYSLIP_WRITE_FIELDS
