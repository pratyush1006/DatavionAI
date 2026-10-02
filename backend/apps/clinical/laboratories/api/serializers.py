from rest_framework import serializers

from ..models import (
    Laboratory,
    LaboratoryOrder,
    LaboratoryOrderItem,
    LaboratoryReport,
    LaboratoryResult,
    LaboratorySlot,
    LaboratorySpecimen,
    LaboratoryTest,
)


class AllFields(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = (
            "id",
            "organization",
            "organization_id",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
        )


class LaboratorySerializer(AllFields):
    class Meta(AllFields.Meta):
        model = Laboratory


class LaboratoryTestSerializer(AllFields):
    class Meta(AllFields.Meta):
        model = LaboratoryTest


class LaboratorySlotSerializer(AllFields):
    class Meta(AllFields.Meta):
        model = LaboratorySlot
        read_only_fields = ("id", "created_at", "updated_at", "booked_count")


class LaboratoryOrderItemSerializer(AllFields):
    class Meta(AllFields.Meta):
        model = LaboratoryOrderItem


class LaboratoryOrderSerializer(AllFields):
    items = LaboratoryOrderItemSerializer(many=True, read_only=True)
    patient_name = serializers.SerializerMethodField()
    laboratory_name = serializers.CharField(source="laboratory.name", read_only=True)

    def get_patient_name(self, obj):
        return getattr(obj.patient, "display_name", None) or str(obj.patient)

    class Meta(AllFields.Meta):
        model = LaboratoryOrder
        read_only_fields = (
            "id",
            "order_number",
            "ordered_at",
            "created_at",
            "updated_at",
        )


class LaboratorySpecimenSerializer(AllFields):
    order_number = serializers.CharField(source="order.order_number", read_only=True)

    class Meta(AllFields.Meta):
        model = LaboratorySpecimen
        read_only_fields = (
            "id",
            "specimen_id",
            "accession_number",
            "barcode",
            "collected_at",
            "created_at",
            "updated_at",
        )


class LaboratoryResultSerializer(AllFields):
    class Meta(AllFields.Meta):
        model = LaboratoryResult
        read_only_fields = (
            "id",
            "entered_at",
            "verified_at",
            "released_at",
            "created_at",
            "updated_at",
        )


class LaboratoryReportSerializer(AllFields):
    class Meta(AllFields.Meta):
        model = LaboratoryReport
        read_only_fields = (
            "id",
            "report_number",
            "released_at",
            "created_at",
            "updated_at",
        )
