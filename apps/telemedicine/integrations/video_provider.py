from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from django.conf import settings
@dataclass(frozen=True,slots=True)
class Room: connection_id:str; connection_url:str; provider_name:str
@dataclass(frozen=True,slots=True)
class ParticipantToken: token:str; expires_at:str|None=None
class VideoProvider(Protocol):
 def create_room(self,*,session_id:str,session_type:str)->Room: ...
 def create_participant_token(self,*,connection_id:str,participant_id:str,display_name:str)->ParticipantToken: ...
 def close_room(self,*,connection_id:str)->None: ...
 def start_recording(self,*,connection_id:str)->str: ...
 def stop_recording(self,*,connection_id:str,recording_id:str)->None: ...
def get_video_provider()->VideoProvider:
 path=getattr(settings,"TELEMEDICINE_VIDEO_PROVIDER","").strip()
 if not path: raise RuntimeError("TELEMEDICINE_VIDEO_PROVIDER is not configured. Configure a concrete WebRTC/video adapter.")
 module_name,class_name=path.rsplit(".",1)
 from importlib import import_module
 return getattr(import_module(module_name),class_name)()
