from rest_framework import serializers

from apps.telemedicine.models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = "__all__"
        read_only_fields = (
            "id",
            "recording_id",
            "status",
            "started_at",
            "finalized_at",
            "created_at",
            "updated_at",
        )
