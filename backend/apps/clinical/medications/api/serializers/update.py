from apps.clinical.medications.api.serializers.base import MedicationBaseSerializer


class MedicationUpdateSerializer(MedicationBaseSerializer):
    class Meta(MedicationBaseSerializer.Meta):
        read_only_fields = tuple(
            set(MedicationBaseSerializer.Meta.read_only_fields)
            | {"organization", "medication_code", "is_active"}
        )
