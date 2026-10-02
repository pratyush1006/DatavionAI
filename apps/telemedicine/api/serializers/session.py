from rest_framework import serializers
from apps.telemedicine.models import TelemedicineSession
class TelemedicineSessionCreateSerializer(serializers.ModelSerializer):
 class Meta: model=TelemedicineSession; fields=("patient","provider","appointment","scheduled_start","scheduled_end","session_type","recording_consent","notes")
 def validate(self,a):
  if a["scheduled_end"]<=a["scheduled_start"]: raise serializers.ValidationError({"scheduled_end":"Session end must be after session start."})
  return a
class TelemedicineSessionUpdateSerializer(serializers.ModelSerializer):
 class Meta: model=TelemedicineSession; fields=("scheduled_start","scheduled_end","session_type","recording_consent","notes")
 def validate(self,a):
  if a.get("scheduled_end",self.instance.scheduled_end)<=a.get("scheduled_start",self.instance.scheduled_start): raise serializers.ValidationError({"scheduled_end":"Session end must be after session start."})
  return a
class TelemedicineSessionDetailSerializer(serializers.ModelSerializer):
 class Meta:
  model=TelemedicineSession; fields="__all__"; read_only_fields=("id","session_id","organization","actual_start","actual_end","status","connection_url","connection_id","provider_name","cancellation_reason","failure_reason","created_at","updated_at")
