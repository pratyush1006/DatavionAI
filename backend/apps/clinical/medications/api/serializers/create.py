from apps.clinical.medications.api.serializers.base import MedicationBaseSerializer


class MedicationCreateSerializer(MedicationBaseSerializer):
    class Meta(MedicationBaseSerializer.Meta):
        read_only_fields = tuple(
            set(MedicationBaseSerializer.Meta.read_only_fields)
            | {"organization", "is_active"}
        )
