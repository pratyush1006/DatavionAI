from rest_framework import serializers

from apps.hospital_operations.models import (
    Bed,
    Facility,
    OPDVisit,
    OperationalUnit,
    Room,
)


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("uuid", "name", "code", "status", "address", "metadata")
        read_only_fields = ("uuid",)


class OperationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalUnit
        fields = (
            "uuid",
            "facility",
            "name",
            "code",
            "unit_type",
            "specialty",
            "active",
            "metadata",
        )
        read_only_fields = ("uuid",)


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = (
            "uuid",
            "room",
            "label",
            "bed_type",
            "status",
            "isolation_capable",
            "active",
            "metadata",
        )
        read_only_fields = ("uuid", "status")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "uuid",
            "facility",
            "unit",
            "number",
            "room_type",
            "floor",
            "status",
            "capacity",
            "metadata",
        )
        read_only_fields = ("uuid",)


class OPDVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPDVisit
        fields = (
            "uuid",
            "patient",
            "queue",
            "token_number",
            "status",
            "registered_at",
            "called_at",
            "consultation_started_at",
            "completed_at",
            "encounter_reference",
        )
        read_only_fields = (
            "uuid",
            "token_number",
            "status",
            "registered_at",
            "called_at",
            "consultation_started_at",
            "completed_at",
        )


class OPDRegistrationSerializer(serializers.Serializer):
    patient = serializers.UUIDField()
    queue = serializers.UUIDField()
    encounter_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=160
    )


class BedReservationCreateSerializer(serializers.Serializer):
    bed = serializers.UUIDField()
    patient = serializers.UUIDField()
    reserved_from = serializers.DateTimeField(required=False)
    reserved_until = serializers.DateTimeField(required=False, allow_null=True)
    reference = serializers.CharField(required=False, allow_blank=True, max_length=120)
    notes = serializers.CharField(required=False, allow_blank=True)


class BedAssignmentCreateSerializer(serializers.Serializer):
    bed = serializers.UUIDField()
    patient = serializers.UUIDField()
    admission_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=120
    )
    reservation = serializers.UUIDField(required=False, allow_null=True)


class AdmissionCreateSerializer(serializers.Serializer):
    patient = serializers.UUIDField()
    unit = serializers.UUIDField()
    bed = serializers.UUIDField()
    admission_number = serializers.CharField(max_length=80)
    reason = serializers.CharField(required=False, allow_blank=True)


class TransferSerializer(serializers.Serializer):
    unit = serializers.UUIDField()
    bed = serializers.UUIDField()
    reason = serializers.CharField(required=False, allow_blank=True)
    icu = serializers.BooleanField(required=False, default=False)
