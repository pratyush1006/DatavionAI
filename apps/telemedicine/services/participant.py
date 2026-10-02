from django.db import transaction
from django.utils import timezone
from apps.telemedicine.constants import ParticipantStatus
from apps.telemedicine.models import Participant
ALLOWED={ParticipantStatus.INVITED:{ParticipantStatus.ADMITTED,ParticipantStatus.REMOVED},ParticipantStatus.ADMITTED:{ParticipantStatus.JOINED,ParticipantStatus.REMOVED},ParticipantStatus.JOINED:{ParticipantStatus.LEFT},ParticipantStatus.LEFT:{ParticipantStatus.JOINED},ParticipantStatus.REMOVED:set()}
class ParticipantService:
 @staticmethod
 @transaction.atomic
 def invite(*,session_id,user_id,participant_type):
  p,created=Participant.objects.get_or_create(session_id=session_id,user_id=user_id,defaults={"participant_type":participant_type,"invited_at":timezone.now()})
  if not created and p.status==ParticipantStatus.REMOVED: p.status=ParticipantStatus.INVITED; p.invited_at=timezone.now(); p.save(update_fields=["status","invited_at","updated_at"])
  return p
 @staticmethod
 @transaction.atomic
 def transition(*,participant_id,organization_id,target_status):
  p=Participant.objects.select_for_update().select_related("session").get(pk=participant_id,session__organization_id=organization_id)
  if target_status not in ALLOWED[p.status]: raise ValueError(f"Invalid participant transition: {p.status} -> {target_status}.")
  now=timezone.now(); p.status=target_status
  if target_status==ParticipantStatus.ADMITTED:p.admitted_at=now
  elif target_status==ParticipantStatus.JOINED:p.joined_at=p.joined_at or now
  elif target_status==ParticipantStatus.LEFT:p.left_at=now
  p.save(update_fields=["status","admitted_at","joined_at","left_at","updated_at"]); return p
 @staticmethod
 @transaction.atomic
 def update_media_state(*,participant_id,organization_id,data):
  p=Participant.objects.select_for_update().select_related("session").get(pk=participant_id,session__organization_id=organization_id)
  if p.status!=ParticipantStatus.JOINED: raise ValueError("Media state can only be updated by a joined participant.")
  p.mark_media_state(**data); p.save(update_fields=["microphone_enabled","camera_enabled","audio_connected","video_connected","microphone_permission","camera_permission","media_updated_at","updated_at"]); return p
