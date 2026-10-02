from rest_framework import serializers

from apps.clinical.encounters.models import Encounter


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = "__all__"
        read_only_fields = (
            "id",
            "status",
            "started_at",
            "ended_at",
            "duration_minutes",
            "is_active",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
            "created_at",
            "updated_at",
        )


class EncounterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = (
            "appointment",
            "patient",
            "provider",
            "encounter_number",
            "chief_complaint",
            "history_of_present_illness",
            "assessment",
            "plan",
            "clinical_notes",
            "is_billable",
        )


class EncounterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = (
            "chief_complaint",
            "history_of_present_illness",
            "assessment",
            "plan",
            "clinical_notes",
            "is_billable",
        )
