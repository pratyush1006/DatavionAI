from rest_framework import serializers
from apps.telemedicine.models import Participant
class ParticipantSerializer(serializers.ModelSerializer):
 class Meta:
  model=Participant; fields=("id","session","user","participant_type","status","invited_at","admitted_at","joined_at","left_at","connection_quality","microphone_enabled","camera_enabled","audio_connected","video_connected","microphone_permission","camera_permission","media_updated_at"); read_only_fields=("id","status","invited_at","admitted_at","joined_at","left_at","media_updated_at")
class ParticipantMediaStateSerializer(serializers.Serializer):
 microphone_enabled=serializers.BooleanField(required=False); camera_enabled=serializers.BooleanField(required=False); audio_connected=serializers.BooleanField(required=False); video_connected=serializers.BooleanField(required=False); microphone_permission=serializers.CharField(required=False); camera_permission=serializers.CharField(required=False)
