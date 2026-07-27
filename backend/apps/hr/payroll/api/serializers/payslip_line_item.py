from rest_framework import serializers

from apps.hr.payroll.models import PayslipLineItem


class PayslipLineItemOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayslipLineItem
        fields = (
            "id",
            "component_type",
            "name",
            "amount",
        )
        read_only_fields = fields


class PayslipLineItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayslipLineItem
        fields = (
            "component_type",
            "name",
            "amount",
        )
