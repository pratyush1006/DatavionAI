"""
Base encounter serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.encounters.models import Encounter


class EncounterBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for encounters.
    """

    class Meta:
        model = Encounter

        fields = (
            "id",
            "organization",
            "appointment",
            "patient",
            "provider",
            "encounter_number",
            "status",
            "chief_complaint",
            "history_of_present_illness",
            "assessment",
            "plan",
            "clinical_notes",
            "started_at",
            "ended_at",
            "duration_minutes",
            "is_billable",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "EncounterBaseSerializer",
]
