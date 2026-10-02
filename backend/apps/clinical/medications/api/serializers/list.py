from apps.clinical.medications.api.serializers.base import MedicationBaseSerializer


class MedicationListSerializer(MedicationBaseSerializer):
    class Meta(MedicationBaseSerializer.Meta):
        fields = (
            "id",
            "medication_code",
            "generic_name",
            "brand_name",
            "strength",
            "strength_unit",
            "dosage_form",
            "route",
            "is_controlled",
            "is_active",
            "display_name",
        )
