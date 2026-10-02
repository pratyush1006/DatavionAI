from rest_framework import serializers

from apps.clinical.diagnoses.models import Diagnosis


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"
        read_only_fields = (
            "id",
            "status",
            "is_active",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
            "created_at",
            "updated_at",
        )


class DiagnosisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = (
            "encounter",
            "diagnosis_code",
            "diagnosis_description",
            "diagnosis_type",
            "is_primary",
            "present_on_admission",
            "notes",
        )


class DiagnosisUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = (
            "diagnosis_description",
            "is_primary",
            "present_on_admission",
            "notes",
        )
