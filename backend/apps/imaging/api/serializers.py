from rest_framework import serializers

from apps.imaging.models import (
    ImagingModality,
    ImagingOrder,
    ImagingProcedure,
    ImagingStudy,
    RadiologyReport,
)


class ImagingModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingModality
        fields = "__all__"
        read_only_fields = (
            "id",
            "tenant_id",
            "organization_id",
            "created_at",
            "updated_at",
        )


class ImagingProcedureSerializer(serializers.ModelSerializer):
    modality_name = serializers.CharField(source="modality.name", read_only=True)

    class Meta:
        model = ImagingProcedure
        fields = "__all__"
        read_only_fields = (
            "id",
            "tenant_id",
            "organization_id",
            "created_at",
            "updated_at",
        )


class ImagingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingOrder
        fields = "__all__"
        read_only_fields = (
            "id",
            "tenant_id",
            "organization_id",
            "status",
            "ordered_at",
            "cancelled_at",
            "created_at",
            "updated_at",
        )


class ImagingStudySerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    procedure_name = serializers.CharField(source="procedure.name", read_only=True)
    modality_name = serializers.CharField(
        source="procedure.modality.name", read_only=True
    )

    class Meta:
        model = ImagingStudy
        fields = "__all__"
        read_only_fields = (
            "id",
            "tenant_id",
            "organization_id",
            "patient_id",
            "status",
            "performed_at",
            "acquired_by_id",
            "created_at",
            "updated_at",
        )


class RadiologyReportSerializer(serializers.ModelSerializer):
    accession_number = serializers.CharField(
        source="study.accession_number", read_only=True
    )
    patient_id = serializers.UUIDField(source="study.patient_id", read_only=True)

    class Meta:
        model = RadiologyReport
        fields = "__all__"
        read_only_fields = (
            "id",
            "tenant_id",
            "organization_id",
            "status",
            "signed_at",
            "version",
            "created_at",
            "updated_at",
        )


class ImagingIdentifierSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class ImagingTransitionSerializer(serializers.Serializer):
    target = serializers.CharField(max_length=64)
