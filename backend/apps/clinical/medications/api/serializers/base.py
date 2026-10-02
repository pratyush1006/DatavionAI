from rest_framework import serializers

from apps.clinical.medications.models import Medication


class MedicationBaseSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Medication
        fields = (
            "id",
            "organization",
            "medication_code",
            "generic_name",
            "brand_name",
            "strength",
            "strength_unit",
            "dosage_form",
            "route",
            "manufacturer",
            "description",
            "is_controlled",
            "is_active",
            "is_deleted",
            "display_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "is_deleted",
            "created_at",
            "updated_at",
            "display_name",
        )
